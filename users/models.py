#Omnichannel-ERP/users/models
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from core.models import Base
class Users(AbstractUser, Base):
    # Override username from AbstractUser (still required for Django)
    username = models.CharField(max_length=150, unique=True)

    city_code_1 = models.CharField(max_length=5, help_text="e.g. +20, +1")
    phone_number_1 = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?\d{7,15}$', "Enter a valid phone number.")],
    )

    city_code_2 = models.CharField(max_length=5, blank=True, null=True)
    phone_number_2 = models.CharField(
        max_length=20,
        blank=True, null=True,
        validators=[RegexValidator(r'^\+?\d{7,15}$', "Enter a valid phone number.")],
    )

    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'
    class Meta:
        db_table = 'users'
    def __str__(self):
        return f"{self.username} ({self.email})"
