from django.contrib import admin
from .models import MortgageApplication


@admin.register(MortgageApplication)
class MortgageApplicationAdmin(admin.ModelAdmin):
    # Настроим отображение столбцов в списке
    list_display = (
        'full_name', 'phone_number', 'city', 'realtor', 'manager' , 'amount', 'down_payment', 'mortgage_term', 'status',
        'created_at'
    )

    # Настроим возможность поиска по полям
    search_fields = (
        'full_name', 'phone_number', 'city', 'realtor__phone_number', 'manager__phone_number'
    )

    # Определим порядок полей в форме добавления/редактирования заявки
    fieldsets = (
        (None, {
            'fields': ('full_name', 'phone_number', 'city')
        }),
        ('Сведения о заявке', {
            'fields': ('amount', 'down_payment', 'mortgage_term', 'status')
        }),
        ('Информация ', {
            'fields': ('realtor', 'manager')
        }),
        ('Дата создания', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    # Ограничим редактирование поля 'created_at' только при создании объекта
    readonly_fields = ('created_at',)

    # Фильтры по статусу
    list_filter = ('status', 'created_at')



