from django.contrib import admin
from .models import *


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'role', 'first_name', 'last_name')
    search_fields = ('phone_number',)

    fieldsets = (
        (None, {
            'fields': ('phone_number', 'role', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'photo')
        }),
    )