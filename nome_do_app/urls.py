from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import CodigoListCreateAPIView

# Definimos o nome do app para referenciação reversa de URLs.
app_name = 'nome_do_app'

# Criamos uma instância de DefaultRouter para registrar nosso ViewSet.
router = DefaultRouter()

# Registramos o ViewSet 'CodigoEntradaViewSet' na rota 'codigos'.
router.register(r'codigos', views.CodigoEntradaViewSet, basename='codigoentrada')

# A lista de padrões de URL do app.
urlpatterns = [
    # Inclui todas as rotas geradas automaticamente pelo router
    path('api/', include(router.urls)),

    # Rota específica para CodigoListCreateAPIView
    path('api/codigos/custom/', CodigoListCreateAPIView.as_view(), name='codigo-list-create'),
]
