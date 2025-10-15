from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """Customer model for CRM"""
    CUSTOMER_TYPE = [
        ('INDIVIDUAL', 'Individual'),
        ('BUSINESS', 'Business'),
    ]
    
    name = models.CharField(max_length=200)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE, default='INDIVIDUAL')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Lead(models.Model):
    """Lead model for potential customers"""
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('CONTACTED', 'Contacted'),
        ('QUALIFIED', 'Qualified'),
        ('CONVERTED', 'Converted'),
        ('LOST', 'Lost'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    source = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='leads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.status}"

    class Meta:
        ordering = ['-created_at']


class Contact(models.Model):
    """Contact model for customer interactions"""
    CONTACT_TYPE = [
        ('EMAIL', 'Email'),
        ('PHONE', 'Phone'),
        ('MEETING', 'Meeting'),
        ('OTHER', 'Other'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts', null=True, blank=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='contacts', null=True, blank=True)
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    contact_date = models.DateTimeField()
    contacted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.contact_date}"

    class Meta:
        ordering = ['-contact_date']
