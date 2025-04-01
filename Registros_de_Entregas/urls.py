# Importa os módulos Django necessários para definir URLs
from django.urls import path, include
# Importa o DefaultRouter do Django REST Framework para criar rotas automáticas para a API
from rest_framework.routers import DefaultRouter
# Importa as views que serão usadas nas rotas
from .views import RegistroEntregaViewSet, RegistroUploadImagesView, RegistroDiagnosticView

# Cria uma instância do roteador que gerará URLs automaticamente para o ViewSet
router = DefaultRouter()
# Registra o RegistroEntregaViewSet com o prefixo 'registros'
# Isso criará automaticamente rotas para as ações CRUD (list, create, retrieve, update, delete)
router.register(r'registros', RegistroEntregaViewSet)

# Define a lista de padrões de URL para a aplicação
urlpatterns = [
    # Inclui todas as URLs geradas pelo roteador
    path('', include(router.urls)),
    # Define uma rota personalizada para upload de imagens para um registro específico
    # A view RegistroUploadImagesView lidará com esta solicitação
    path('registros/<str:pk>/upload_images/', RegistroUploadImagesView.as_view(), name='registro-upload-images'),
    # Define uma rota personalizada para diagnóstico de um registro específico
    # A view RegistroDiagnosticView lidará com esta solicitação
    path('registros/<str:pk>/diagnostic/', RegistroDiagnosticView.as_view(), name='registro-diagnostic'),
    # A ação 'images' é automaticamente incluída pelo roteador e não precisa ser definida aqui
]
