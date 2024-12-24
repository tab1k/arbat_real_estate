from django.contrib import admin
from .models import *


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'email', 'date_of_birth', 'photo')
    search_fields = ('phone_number', 'email')
    list_filter = ('date_of_birth',)


admin.site.register(CustomUser, CustomUserAdmin)
