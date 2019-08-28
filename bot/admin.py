from django.contrib import admin

from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'username',
        'track',
        'session',
        'access_count',
        'updated_at',
        'created_at'
    )
    list_display_link = ('id', 'first_name')
    list_filter = ('is_manually_added', )
    search_fields = ('username', 'first_name', 'last_name')
    readonly_fields = ('access_count', 'updated_at', 'created_at')
