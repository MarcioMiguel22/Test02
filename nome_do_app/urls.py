from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'nome_do_app'

router = DefaultRouter()
router.register(r'codigos', views.CodigoEntradaViewSet, basename='codigoentrada')

urlpatterns = [
    path('', views.home, name='home'),  # Add the home view as root URL
    path('api/', include(router.urls)),  # Keep the API URLs under /api/
    path('codigos/', views.CodigoEntradaViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('codigos/<int:pk>/', views.CodigoEntradaViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]



