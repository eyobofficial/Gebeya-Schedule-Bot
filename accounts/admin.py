from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'telegram_id',
        'is_active',
        'is_staff',
        'is_superuser'
    )
    list_display_link = ('username', 'first_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_manually_added')
    search_fields = ('username', 'first_name', 'telegram_id')
