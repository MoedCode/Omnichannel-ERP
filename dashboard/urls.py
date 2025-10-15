from django.urls import path
from . import views

urlpatterns = [
    path('overview/', views.DashboardOverviewView.as_view(), name='dashboard-overview'),
    path('reports/sales/', views.SalesReportView.as_view(), name='sales-report'),
    path('reports/inventory/', views.InventoryReportView.as_view(), name='inventory-report'),
]
