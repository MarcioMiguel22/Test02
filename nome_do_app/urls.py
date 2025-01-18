from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CodigoEntradaViewSet

router = DefaultRouter()
router.register(r'codigos', CodigoEntradaViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
