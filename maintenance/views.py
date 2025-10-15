from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Asset, WorkOrder
from .serializers import AssetSerializer, WorkOrderSerializer


class AssetViewSet(viewsets.ModelViewSet):
    """API endpoint for managing assets"""
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'customer']
    search_fields = ['name', 'asset_tag']
    ordering_fields = ['name', 'purchase_date']


class WorkOrderViewSet(viewsets.ModelViewSet):
    """API endpoint for managing work orders"""
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'assigned_to', 'customer', 'asset']
    search_fields = ['order_number', 'title', 'description']
    ordering_fields = ['scheduled_date', 'created_at', 'priority']
