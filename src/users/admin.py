from django.contrib import admin
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('phone_number', 'role', 'first_name', 'last_name')
    search_fields = ('phone_number',)

    ordering = ('phone_number',)  # Замените на нужное поле

    fieldsets = (
        (None, {
            'fields': ('phone_number', 'role', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'photo')
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.password:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)
