from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistroEntregaViewSet, RegistroUploadImagesView

router = DefaultRouter()
router.register(r'registros', RegistroEntregaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('registros/<str:pk>/upload_images/', RegistroUploadImagesView.as_view(), name='registro-upload-images'),
]
