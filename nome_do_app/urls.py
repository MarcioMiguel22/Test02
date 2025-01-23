#URLS

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import CodigoListCreateAPIView, LocalDeChavesAPIView, AdministracaoAPIView, HomeView

# Definimos o nome do app para referenciação reversa de URLs.
app_name = 'nome_do_app'

# Criamos uma instância de DefaultRouter para registrar nosso ViewSet.
router = DefaultRouter()

# Registramos o ViewSet 'CodigoEntradaViewSet' na rota 'api/codigos'.
router.register(r'codigos', views.CodigoEntradaViewSet, basename='codigoentrada')

# A lista de padrões de URL do app.
urlpatterns = [
    # Inclui todas as rotas geradas automaticamente pelo router
    path('api/', include(router.urls)),

    # Rota específica para CodigoListCreateAPIView
    path('api/codigos/custom/', CodigoListCreateAPIView.as_view(), name='codigo-list-create'),

    # Rota específica para atualizar uma instância de CodigoEntrada
    path('api/codigos/<int:pk>/', views.CodigoEntradaDetailAPIView.as_view(), name='codigo-detail'),

    # Rota específica para LocalDeChavesAPIView
    path('api/local_de_chaves/', LocalDeChavesAPIView.as_view(), name='local-de-chaves'),
    
    # Rota específica para AdministracaoAPIView
    path('api/administracao/', AdministracaoAPIView.as_view(), name='administracao'),

    # Rota específica para HomeView
    path('', HomeView.as_view(), name='home'),
]
