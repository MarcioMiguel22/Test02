# O módulo django.urls é responsável por gerenciar as rotas do projeto Django.
# A função path é usada para definir caminhos de URL (endpoints) para suas views.
# O include permite incluir outros conjuntos de URLs dentro de um único arquivo
# de configuração.

from django.urls import path, include

# O DefaultRouter do Django Rest Framework gera automaticamente as URLs para
# as rotas do ViewSet (como list, create, retrieve, update, delete) sem que
# precisemos definir manualmente todas elas.
from rest_framework.routers import DefaultRouter

# Importamos nossas views, especificamente o viewset 'CodigoEntradaViewSet'.
from . import views

# Definimos o nome do app para referenciação reversa de URLs.
app_name = 'nome_do_app'

# Criamos uma instância de DefaultRouter para registrar nosso viewset.
router = DefaultRouter()

# Registramos o viewset 'CodigoEntradaViewSet' na rota 'codigos', com
# o basename 'codigoentrada'. Isso fará com que tenhamos, por exemplo:
# - GET /api/codigos/
# - POST /api/codigos/
# - GET /api/codigos/<id>/
# - etc.
router.register(r'codigos', views.CodigoEntradaViewSet, basename='codigoentrada')

# A lista de padrões de URL do app. Aqui, definimos que quando acessarmos
# o caminho 'api/', incluiremos todas as rotas geradas pelo 'router'.
urlpatterns = [
    path('api/', include(router.urls)),
    path('some-endpoint/', views.some_view, name='some_view'),  # Exemplo de endpoint
]
