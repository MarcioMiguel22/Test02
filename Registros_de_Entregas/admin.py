from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import RegistroEntrega

@admin.register(RegistroEntrega)
class RegistroEntregaAdmin(admin.ModelAdmin):
    list_display = ['numero_obra', 'numero_instalacao', 'data_entrega', 'criado_em']
    list_filter = ['data_entrega']
    search_fields = ['numero_obra', 'numero_instalacao']
    date_hierarchy = 'data_entrega'
