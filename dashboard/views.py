from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q, F
from django.db import models
from django.utils import timezone
from datetime import timedelta

from inventory.models import Product
from crm.models import Customer, Lead
from sales.models import Order
from accounting.models import Invoice, Expense


class DashboardOverviewView(APIView):
    """Dashboard overview with key metrics"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        last_30_days = today - timedelta(days=30)

        # Sales metrics
        total_orders = Order.objects.count()
        orders_last_30_days = Order.objects.filter(created_at__date__gte=last_30_days).count()
        total_revenue = Order.objects.filter(status='COMPLETED').aggregate(total=Sum('total'))['total'] or 0
        revenue_last_30_days = Order.objects.filter(
            status='COMPLETED',
            created_at__date__gte=last_30_days
        ).aggregate(total=Sum('total'))['total'] or 0

        # Customer metrics
        total_customers = Customer.objects.count()
        new_customers_last_30_days = Customer.objects.filter(created_at__date__gte=last_30_days).count()

        # Lead metrics
        total_leads = Lead.objects.count()
        active_leads = Lead.objects.filter(status__in=['NEW', 'CONTACTED', 'QUALIFIED']).count()

        # Inventory metrics
        total_products = Product.objects.count()
        low_stock_products = Product.objects.filter(
            quantity_in_stock__lte=F('reorder_level')
        ).count()

        # Invoice metrics
        pending_invoices = Invoice.objects.filter(status__in=['DRAFT', 'SENT']).count()
        overdue_invoices = Invoice.objects.filter(status='OVERDUE').count()

        # Expense metrics
        expenses_last_30_days = Expense.objects.filter(
            expense_date__gte=last_30_days
        ).aggregate(total=Sum('amount'))['total'] or 0

        data = {
            'sales': {
                'total_orders': total_orders,
                'orders_last_30_days': orders_last_30_days,
                'total_revenue': float(total_revenue),
                'revenue_last_30_days': float(revenue_last_30_days),
            },
            'customers': {
                'total_customers': total_customers,
                'new_customers_last_30_days': new_customers_last_30_days,
            },
            'leads': {
                'total_leads': total_leads,
                'active_leads': active_leads,
            },
            'inventory': {
                'total_products': total_products,
                'low_stock_products': low_stock_products,
            },
            'accounting': {
                'pending_invoices': pending_invoices,
                'overdue_invoices': overdue_invoices,
                'expenses_last_30_days': float(expenses_last_30_days),
            }
        }

        return Response(data)


class SalesReportView(APIView):
    """Sales reports and analytics"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Sales by status
        sales_by_status = Order.objects.values('status').annotate(
            count=Count('id'),
            total=Sum('total')
        )

        # Sales by type (POS vs Online)
        sales_by_type = Order.objects.values('order_type').annotate(
            count=Count('id'),
            total=Sum('total')
        )

        data = {
            'sales_by_status': list(sales_by_status),
            'sales_by_type': list(sales_by_type),
        }

        return Response(data)


class InventoryReportView(APIView):
    """Inventory reports and analytics"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Products by category
        products_by_category = Product.objects.values('category__name').annotate(
            count=Count('id'),
            total_value=Sum(F('quantity_in_stock') * F('cost_price'))
        )

        # Low stock alerts
        low_stock = Product.objects.filter(
            quantity_in_stock__lte=F('reorder_level')
        ).values('name', 'sku', 'quantity_in_stock', 'reorder_level')

        data = {
            'products_by_category': list(products_by_category),
            'low_stock_alerts': list(low_stock),
        }

        return Response(data)
