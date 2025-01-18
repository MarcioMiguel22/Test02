from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'nome_do_app'

router = DefaultRouter()
router.register(r'codigos', views.CodigoEntradaViewSet, basename='codigoentrada')

urlpatterns = [
    path('api/', include(router.urls)),
]
