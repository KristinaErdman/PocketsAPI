from django.contrib.admin import ModelAdmin, register
from .models import CustomUser


@register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = ('id', 'username', 'email')
    list_display_links = ('username', )
    ordering = ('-date_joined', )
    readonly_fields = ('date_joined', 'last_login', )
