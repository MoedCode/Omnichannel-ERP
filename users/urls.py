# users/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
     path('profile', ProfileRetrieveUpdateView.as_view(), name='profile'),
    # path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
