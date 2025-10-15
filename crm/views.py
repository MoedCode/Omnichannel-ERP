from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer, Lead, Contact
from .serializers import CustomerSerializer, LeadSerializer, ContactSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """API endpoint for managing customers"""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer_type', 'city', 'country']
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name', 'created_at']


class LeadViewSet(viewsets.ModelViewSet):
    """API endpoint for managing leads"""
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'assigned_to']
    search_fields = ['name', 'email', 'company']
    ordering_fields = ['created_at', 'updated_at']


class ContactViewSet(viewsets.ModelViewSet):
    """API endpoint for managing contacts"""
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['customer', 'lead', 'contact_type']
    ordering_fields = ['contact_date', 'created_at']

    def perform_create(self, serializer):
        serializer.save(contacted_by=self.request.user)
