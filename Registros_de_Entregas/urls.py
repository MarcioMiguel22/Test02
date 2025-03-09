from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistroEntregaViewSet

router = DefaultRouter()
router.register(r'registros', RegistroEntregaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
