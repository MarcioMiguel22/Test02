from django.contrib import admin
from .models import CodigoEntrada

@admin.register(CodigoEntrada)
class CodigoEntradaAdmin(admin.ModelAdmin):
    list_display = ('id', 'localizacao', 'instalacao')
    search_fields = ('localizacao', 'instalacao')
    list_filter = ('localizacao',)
