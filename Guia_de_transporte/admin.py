"""
Documento de Administração para Guia de Transporte.
Configura a interface de administração do Django para os modelos da aplicação,
incluindo customizações como campos de exibição, filtros e busca.
"""
from django.contrib import admin
from .models import GuiaDeTransporte, TransportItem

# Registro customizado do modelo GuiaDeTransporte
@admin.register(GuiaDeTransporte)
class GuiaDeTransporteAdmin(admin.ModelAdmin):
    list_display = ('item', 'descricao', 'quantidade', 'quantidade_total', 'em_falta', 'total', 'username', 'created_at')
    search_fields = ('item', 'descricao', 'username')
    list_filter = ('created_at', 'em_falta', 'total', 'username')

# Registro do modelo TransportItem
@admin.register(TransportItem)
class TransportItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'descricao', 'unidade', 'quantidade', 'quantidade_total', 'em_falta', 'total', 'current_user')
    search_fields = ('item', 'descricao', 'current_user')
    list_filter = ('unidade', 'em_falta', 'current_user')
