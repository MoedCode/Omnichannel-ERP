from django.contrib import admin
from .models import Asset, WorkOrder


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'asset_tag', 'customer', 'status', 'purchase_date', 'warranty_expiry']
    list_filter = ['status', 'purchase_date']
    search_fields = ['name', 'asset_tag']


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'title', 'asset', 'customer', 'status', 'priority', 'assigned_to', 'scheduled_date']
    list_filter = ['status', 'priority', 'assigned_to']
    search_fields = ['order_number', 'title', 'description']
