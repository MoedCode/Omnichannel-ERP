from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'assets', views.AssetViewSet)
router.register(r'work-orders', views.WorkOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
