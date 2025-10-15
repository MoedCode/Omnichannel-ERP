from django.db import models
from django.contrib.auth.models import User
from crm.models import Customer
from sales.models import Order


class Invoice(models.Model):
    """Invoice model for billing"""
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SENT', 'Sent'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    invoice_number = models.CharField(max_length=50, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice', null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.invoice_number} - {self.customer.name}"

    class Meta:
        ordering = ['-created_at']


class Account(models.Model):
    """Chart of accounts"""
    ACCOUNT_TYPE = [
        ('ASSET', 'Asset'),
        ('LIABILITY', 'Liability'),
        ('EQUITY', 'Equity'),
        ('REVENUE', 'Revenue'),
        ('EXPENSE', 'Expense'),
    ]
    
    account_number = models.CharField(max_length=20, unique=True)
    account_name = models.CharField(max_length=200)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_number} - {self.account_name}"

    class Meta:
        ordering = ['account_number']


class LedgerEntry(models.Model):
    """General ledger entries"""
    ENTRY_TYPE = [
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    ]
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='entries')
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    reference = models.CharField(max_length=100, blank=True)
    transaction_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.account_name} - {self.entry_type} - {self.amount}"

    class Meta:
        verbose_name_plural = "Ledger Entries"
        ordering = ['-transaction_date']


class Expense(models.Model):
    """Expense tracking"""
    CATEGORY_CHOICES = [
        ('SUPPLIES', 'Supplies'),
        ('UTILITIES', 'Utilities'),
        ('RENT', 'Rent'),
        ('SALARIES', 'Salaries'),
        ('MARKETING', 'Marketing'),
        ('OTHER', 'Other'),
    ]
    
    expense_number = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    expense_date = models.DateField()
    paid_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expense_number} - {self.category} - {self.amount}"

    class Meta:
        ordering = ['-expense_date']
