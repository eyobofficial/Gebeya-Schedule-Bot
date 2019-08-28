from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    list_display_link = ('username', )
    list_filter = ('is_active', 'is_staff', 'is_superuser', )
    search_fields = ('username', 'first_name', 'last_name')
