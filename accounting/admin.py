from django.contrib import admin
from .models import Invoice, Account, LedgerEntry, Expense


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer', 'issue_date', 'due_date', 'status', 'total']
    list_filter = ['status', 'issue_date']
    search_fields = ['invoice_number', 'customer__name']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'account_name', 'account_type', 'is_active']
    list_filter = ['account_type', 'is_active']
    search_fields = ['account_number', 'account_name']


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ['account', 'entry_type', 'amount', 'transaction_date', 'created_by']
    list_filter = ['entry_type', 'transaction_date']
    search_fields = ['account__account_name', 'description']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['expense_number', 'category', 'amount', 'expense_date', 'paid_by']
    list_filter = ['category', 'expense_date']
    search_fields = ['expense_number', 'description']
