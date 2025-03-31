from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for viewsets
router = DefaultRouter()
router.register(r'rates', views.RatesConfigurationViewSet)

urlpatterns = [
    path('', views.AvariaListCreate.as_view(), name='avarias-list-create'),
    path('<int:pk>/', views.AvariaRetrieveUpdateDestroy.as_view(), name='avarias-retrieve-update-destroy'),
    path('materiais/', views.MaterialListCreate.as_view(), name='materiais-list-create'),
    path('materiais/<int:pk>/', views.MaterialRetrieveUpdateDestroy.as_view(), name='materiais-retrieve-update-destroy'),
    path('', include(router.urls)),
]
