from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import UserProfile

# Exibir o perfil inline junto com o usuário
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil do Usuário'
    fk_name = 'user'

# Personalizar a visualização do modelo User no admin
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'last_login')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    ordering = ('-date_joined',)
    
    # Ações personalizadas
    actions = ['activate_users', 'deactivate_users']
    
    # Campos nas seções de detalhes (fieldsets)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    def activate_users(self, request, queryset):
        """Ação para ativar usuários selecionados"""
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} usuários foram ativados com sucesso.")
    activate_users.short_description = "Ativar usuários selecionados"
    
    def deactivate_users(self, request, queryset):
        """Ação para desativar usuários selecionados"""
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} usuários foram desativados com sucesso.")
    deactivate_users.short_description = "Desativar usuários selecionados"

# Se quiser criar um admin personalizado com branding próprio
class CustomAdminSite(admin.AdminSite):
    site_header = 'Sistema de Administração'
    site_title = 'Portal Admin'
    index_title = 'Bem-vindo ao Portal de Administração'

# Desregistrar o UserAdmin padrão e registrar o nosso personalizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Para usar o admin site personalizado, descomente estas linhas:
# custom_admin_site = CustomAdminSite(name='customadmin')
# custom_admin_site.register(User, CustomUserAdmin)
# # E use custom_admin_site.urls em seu urls.py principal
