from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer, OrderItemSerializer, PaymentSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """API endpoint for managing orders (POS and Online)"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['order_type', 'status', 'payment_status', 'customer']
    search_fields = ['order_number']
    ordering_fields = ['created_at', 'total']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def pos_orders(self, request):
        """Get POS orders only"""
        pos_orders = self.get_queryset().filter(order_type='POS')
        serializer = self.get_serializer(pos_orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def online_orders(self, request):
        """Get online orders only"""
        online_orders = self.get_queryset().filter(order_type='ONLINE')
        serializer = self.get_serializer(online_orders, many=True)
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    """API endpoint for managing order items"""
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'product']


class PaymentViewSet(viewsets.ModelViewSet):
    """API endpoint for managing payments"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['order', 'payment_method']
    ordering_fields = ['created_at', 'amount']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
