from django.contrib import admin
from .models import Informacao, GuiaDeTransporte

admin.site.register(Informacao)

@admin.register(GuiaDeTransporte)
class GuiaDeTransporteAdmin(admin.ModelAdmin):
    list_display = ('item', 'descricao', 'unidade', 'quantidade', 'created_at')
    search_fields = ('item', 'descricao')
    list_filter = ('created_at', 'unidade')
