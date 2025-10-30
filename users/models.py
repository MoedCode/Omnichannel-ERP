
#users/models.py
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from core.models import Base


class User(AbstractUser, Base):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, help_text="Password (will be hashed automatically)")
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    address = models.CharField(max_length=255, blank=True, null=True)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f"{self.username} ({self.email})"

    # ------------------------------------------------
    # ✅ Custom SAVE method with validation
    # ------------------------------------------------
    def save(self, *args, **kwargs):
        if not self.email:
            raise ValidationError("Email is required for every user.")
        if not self.username:
            raise ValidationError("Username cannot be empty.")

        # Example: normalize email before saving
        self.email = self.email.lower().strip()

        super().save(*args, **kwargs)

    # ------------------------------------------------
    # ✅ UPDATE user fields safely
    # ------------------------------------------------
    def update(self, **kwargs):
        allowed_fields = ['email', 'city', 'country', 'postal_code', 'address', 'first_name', 'last_name']
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(self, field, value)
        self.save()
        return self

    # ------------------------------------------------
    # ✅ DELETE user safely (also removes phone numbers)
    # ------------------------------------------------
    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.phone_numbers.all().delete()
            super().delete(*args, **kwargs)


class PhoneNumber(Base):
    """
    Each user can have multiple phone numbers.
    Type can be: primary, whatsapp, telegram, etc.
    """
    TYPE_CHOICES = [
        ('primary', 'Primary'),
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="phone_numbers")
    country_code = models.CharField(max_length=5, help_text="e.g. +20, +1")
    number = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?\d{7,15}$', "Enter a valid phone number.")],
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='primary')
    verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'phone_number'
        unique_together = ('user', 'number')

    def __str__(self):
        return f"{self.user.username} - {self.type}: {self.country_code}{self.number}"

    # ------------------------------------------------
    # ✅ Custom SAVE with validation
    # ------------------------------------------------
    def save(self, *args, **kwargs):
        if not self.number:
            raise ValidationError("Phone number cannot be empty.")
        if not self.country_code.startswith("+"):
            raise ValidationError("Country code must start with '+'.")
        super().save(*args, **kwargs)

    # ------------------------------------------------
    # ✅ UPDATE phone number fields
    # ------------------------------------------------
    def update(self, **kwargs):
        allowed_fields = ['country_code', 'number', 'type', 'verified']
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(self, field, value)
        self.save()
        return self

    # ------------------------------------------------
    # ✅ DELETE safely
    # ------------------------------------------------
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

class Profile(Base):
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="profile"
    )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    is_public = models.BooleanField(default=True)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return f"Profile of {self.user.username}"

    def save(self, *args, **kwargs):
        # Delete old image if a new one is uploaded
        if self.pk:
            old = Profile.objects.filter(pk=self.pk).first()
            if old and old.profile_image and old.profile_image != self.profile_image:
                old.profile_image.delete(save=False)

        if not self.user_id:
            raise ValidationError("Profile must be linked to a valid user.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete image from disk when profile is deleted
        if self.profile_image:
            self.profile_image.delete(save=False)
        super().delete(*args, **kwargs)