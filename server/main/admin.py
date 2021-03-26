from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from main import models 

class UserAdmin(BaseUserAdmin):
    ordering=['id']
    list_display=["username", "adminApproval", "id", "type"]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Approval Status'), {'fields': ('adminApproval',)}),
        (_('Host'), {'fields': ('host',)}),
        (_('URL'), {'fields': ('url',)}),
        (_('Author Info'), {'fields': ('displayName', 'github')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
    )


admin.site.register(models.Author, UserAdmin)
