from django.contrib import admin
from .models import Avaria, Material

@admin.register(Avaria)
class AvariaAdmin(admin.ModelAdmin):
    list_display = ['localizacao', 'instalacao', 'data_da_avaria', 'estado_do_elevador', 'current_user']
    search_fields = ['localizacao', 'instalacao', 'current_user']
    list_filter = ['estado_do_elevador', 'current_user']

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao']
    search_fields = ['codigo', 'descricao']
