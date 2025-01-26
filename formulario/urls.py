from django.urls import path
from .views import salvar_respostas, obter_respostas

urlpatterns = [
    path('salvar/', salvar_respostas, name='salvar_respostas'),
    path('obter/<str:numero_instalacao>/', obter_respostas, name='obter_respostas'),
]
