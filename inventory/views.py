from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Supplier, Category, Product, StockMovement
from .serializers import (
    SupplierSerializer, CategorySerializer,
    ProductSerializer, StockMovementSerializer
)


class SupplierViewSet(viewsets.ModelViewSet):
    """API endpoint for managing suppliers"""
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'contact_person']
    ordering_fields = ['name', 'created_at']


class CategoryViewSet(viewsets.ModelViewSet):
    """API endpoint for managing product categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class ProductViewSet(viewsets.ModelViewSet):
    """API endpoint for managing products"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'supplier', 'status']
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['name', 'created_at', 'selling_price', 'quantity_in_stock']

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get products with low stock levels"""
        low_stock_products = [p for p in self.get_queryset() if p.is_low_stock]
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)


class StockMovementViewSet(viewsets.ModelViewSet):
    """API endpoint for managing stock movements"""
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'movement_type']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
