from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuiaDeTransporteViewSet

router = DefaultRouter()
router.register(r'guias', GuiaDeTransporteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
