from rest_framework import serializers
from .models import Asset, WorkOrder


class AssetSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    
    class Meta:
        model = Asset
        fields = '__all__'


class WorkOrderSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    
    class Meta:
        model = WorkOrder
        fields = '__all__'
