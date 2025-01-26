from django.urls import path
from .views import salvar_respostas, obter_respostas, obter_todas_respostas, criar_instalacao, deletar_respostas

urlpatterns = [
    path('salvar/', salvar_respostas, name='salvar_respostas'),
    path('obter/<str:numero_instalacao>/', obter_respostas, name='obter_respostas'),
    path('obter_todas/', obter_todas_respostas, name='obter_todas_respostas'),
    path('criar/', criar_instalacao, name='criar_instalacao'),
    path('deletar/<str:numero_instalacao>/', deletar_respostas, name='deletar_respostas'),  # Nova rota para DELETE
]
