from django.urls import path
from .views import (
    login_view, 
    register_view, 
    request_password_reset, 
    reset_password,
    user_profile_view,
    change_password_view,
    delete_account_view
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/login/', login_view, name='login'),
    path('auth/register/', register_view, name='register'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/password/reset/request/', request_password_reset, name='password_reset_request'),
    path('auth/password/reset/confirm/', reset_password, name='password_reset_confirm'),
    path('users/profile/', user_profile_view, name='user_profile'),
    path('users/change-password/', change_password_view, name='change_password'),
    path('users/delete-account/', delete_account_view, name='delete_account'),
]