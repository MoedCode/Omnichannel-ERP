from rest_framework import serializers
from .models import Customer, Lead, Contact


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class LeadSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    
    class Meta:
        model = Lead
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    lead_name = serializers.CharField(source='lead.name', read_only=True)
    contacted_by_username = serializers.CharField(source='contacted_by.username', read_only=True)
    
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ('contacted_by', 'created_at')
