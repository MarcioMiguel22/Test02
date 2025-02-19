from django.urls import path
from . import views  # Corrected import

urlpatterns = [
    path('', views.AvariaListCreate.as_view(), name='avarias-list-create'),
    path('<int:pk>/', views.AvariaRetrieveUpdateDestroy.as_view(), name='avarias-retrieve-update-destroy'),
    path('materiais/', views.MaterialListCreate.as_view(), name='materiais-list-create'),
    path('materiais/<int:pk>/', views.MaterialRetrieveUpdateDestroy.as_view(), name='materiais-retrieve-update-destroy'),
]
