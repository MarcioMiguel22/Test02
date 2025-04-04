from django.contrib import admin
from .models import RegistroEntrega

@admin.register(RegistroEntrega)
class RegistroEntregaAdmin(admin.ModelAdmin):
    list_display = ['numero_obra', 'numero_instalacao', 'data_entrega', 'data_criacao', 'criado_em', 'criado_por']
    list_filter = ['data_entrega', 'data_criacao', 'criado_por']
    search_fields = ['numero_obra', 'numero_instalacao', 'notas']
    date_hierarchy = 'data_entrega'
    raw_id_fields = ['criado_por']
