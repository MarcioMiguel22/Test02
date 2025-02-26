
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InformacaoViewSet

router = DefaultRouter()
router.register(r'informacoes', InformacaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
