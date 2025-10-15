from django.contrib import admin
from .models import Customer, Lead, Contact


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'customer_type', 'email', 'phone', 'city', 'created_at']
    list_filter = ['customer_type', 'city', 'country']
    search_fields = ['name', 'email', 'phone']


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'status', 'assigned_to', 'created_at']
    list_filter = ['status', 'assigned_to']
    search_fields = ['name', 'email', 'company']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['subject', 'contact_type', 'customer', 'lead', 'contact_date', 'contacted_by']
    list_filter = ['contact_type', 'contact_date']
    search_fields = ['subject', 'description']
