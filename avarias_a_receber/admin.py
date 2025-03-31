from django.contrib import admin
from .models import Avaria, Material, RatesConfiguration

@admin.register(Avaria)
class AvariaAdmin(admin.ModelAdmin):
    list_display = ['localizacao', 'instalacao', 'data_da_avaria', 'estado_do_elevador', 'current_user']
    search_fields = ['localizacao', 'instalacao', 'current_user']
    list_filter = ['estado_do_elevador', 'current_user']

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao']
    search_fields = ['codigo', 'descricao']

@admin.register(RatesConfiguration)
class RatesConfigurationAdmin(admin.ModelAdmin):
    list_display = ['current_user', 'standard_rate', 'stop_rate', 'after_11pm_surcharge']
    search_fields = ['current_user']
