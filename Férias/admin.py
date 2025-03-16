from django.contrib import admin
from .models import Vacation

@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date')
    search_fields = ('employee_name', 'notes')
