from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Invoice, Account, LedgerEntry, Expense
from .serializers import (
    InvoiceSerializer, AccountSerializer,
    LedgerEntrySerializer, ExpenseSerializer
)


class InvoiceViewSet(viewsets.ModelViewSet):
    """API endpoint for managing invoices"""
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'customer']
    search_fields = ['invoice_number']
    ordering_fields = ['issue_date', 'due_date', 'total']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AccountViewSet(viewsets.ModelViewSet):
    """API endpoint for managing accounts"""
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['account_type', 'is_active']
    search_fields = ['account_number', 'account_name']


class LedgerEntryViewSet(viewsets.ModelViewSet):
    """API endpoint for managing ledger entries"""
    queryset = LedgerEntry.objects.all()
    serializer_class = LedgerEntrySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['account', 'entry_type']
    ordering_fields = ['transaction_date', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    """API endpoint for managing expenses"""
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'paid_by']
    search_fields = ['expense_number', 'description']
    ordering_fields = ['expense_date', 'amount']
