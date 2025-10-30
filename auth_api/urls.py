from django.urls import path
from auth_api.views  import *

urlpatterns = [
    path('login/', SessionLoginView.as_view(), name='session-login'),
    path('logout/', SessionLogoutView.as_view(), name='session-logout'),
    # path("access", GetAccessTokenView.as_view(), "access-token"),
    # path("refresh", GetRefreshTokenView.as_view(), "refresh-token"),
]