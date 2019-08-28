from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'telegram_id',
        'track',
        'session',
        'is_active',
        'is_staff',
        'is_superuser',
        'access_count'
    )
    list_display_link = ('username', 'first_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_manually_added')
    search_fields = ('username', 'first_name', 'telegram_id')
    readonly_fields = ('access_count', 'updated_at')
