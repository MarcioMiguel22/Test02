from django.contrib import admin
from .models import DespesaCarro

@admin.register(DespesaCarro)
class DespesaCarroAdmin(admin.ModelAdmin):
    list_display = ('tipo_combustivel', 'valor_despesa', 'data_despesa', 'quilometragem', 'usuario')
    list_filter = ('tipo_combustivel', 'data_despesa', 'usuario')
    search_fields = ('tipo_combustivel', 'observacoes', 'usuario__username')
    date_hierarchy = 'data_despesa'
    readonly_fields = ('id', 'data_criacao', 'data_atualizacao', 'usuario_criacao')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'tipo_combustivel', 'valor_despesa', 'data_despesa', 'quilometragem')
        }),
        ('Detalhes Adicionais', {
            'fields': ('observacoes', 'imagem', 'imagens')
        }),
        ('Metadados', {
            'fields': ('id', 'data_criacao', 'data_atualizacao', 'usuario_criacao'),
            'classes': ('collapse',)
        }),
    )
