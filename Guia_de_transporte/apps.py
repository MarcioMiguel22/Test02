"""
Documento de Configuração do Aplicativo Guia de Transporte.
Define as configurações básicas da aplicação Django para Guia de Transporte,
como o campo de auto incremento padrão e o nome do aplicativo.
"""
from django.apps import AppConfig


class GuiaDeTransporteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Guia_de_transporte'
