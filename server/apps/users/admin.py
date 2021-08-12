from django.contrib.admin import ModelAdmin, register
from ..money.admin import CategoryInline
from .models import CustomUser


@register(CustomUser)
class UserAdmin(ModelAdmin):
    list_display = ('id', 'username', 'email')
    list_display_links = ('username', )
    ordering = ('-date_joined', )
    fieldsets = (
        ('Основные сведения', {
            'fields': (('first_name', 'last_name'), ('username', 'email'), 'password',
                       ('date_joined', 'last_login')),
        }
         ),
        ('Статус и права доступа', {
            'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions'),
        }),
    )
    inlines = [CategoryInline, ]
    readonly_fields = ('date_joined', 'last_login', )
