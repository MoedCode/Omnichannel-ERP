from django.urls import path
from auth_api.sessions_views  import *
from .views import *
urlpatterns = [
    # path('login/', SessionLoginView.as_view(), name='session-login'),
    # path('logout/', SessionLogoutView.as_view(), name='session-logout'),
    path("login/", JWTLoginView.as_view(), name="jwt-login"),
    path("logout/", JWTLogoutView.as_view(), name="jwt-logout"),
     path('refresh/', JWTRefreshView.as_view(), name='jwt-refresh'),
]