from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VacationViewSet

router = DefaultRouter()
router.register(r'', VacationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
