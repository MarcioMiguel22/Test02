from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password/reset/request/', views.request_password_reset, name='request_password_reset'),
    path('password/reset/confirm/', views.reset_password, name='reset_password'),
]