from django.urls import path

from backend import views
from .views import salvar_respostas, obter_respostas

urlpatterns = [
    path('salvar/', salvar_respostas, name='salvar_respostas'),
    path('formulario/salvar/', views.salvar_formulario, name='salvar_formulario'),
]
