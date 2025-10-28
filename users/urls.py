# users/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    # path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
