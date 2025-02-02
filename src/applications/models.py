from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model

from users.models import CustomUser


class MortgageApplication(models.Model):
    STATUS_CHOICES = (
        ('in_work', 'В работе'),
        ('first_approved', 'Первоначальное одобрение'),
        ('approved', 'Одобрено'),
        ('rejected', 'Не одобрено'),
    )

    realtor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name="Риэлтор"
    )
    manager = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='managed_applications',
        blank=True,
        null=True,
        verbose_name="Менеджер"
    )

    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    iin = models.PositiveBigIntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=25, verbose_name='Номер телефона')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма ипотеки')
    down_payment = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Первоначальный взнос')
    mortgage_term = models.IntegerField(verbose_name='Срок ипотеки')
    city = models.CharField(max_length=100, verbose_name='Город')

    status = models.CharField(choices=STATUS_CHOICES, blank=True, max_length=50, default='in_work', verbose_name='Статус')

    code = models.CharField(max_length=10, blank=True, null=True, verbose_name='Код заявки')
    code_requested = models.BooleanField(default=False, verbose_name="Код запрошен")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    def __str__(self):
        return f'Заявка от {self.full_name} ({self.phone_number})'

    def assign_manager(self, manager):
        """
        Привязать заявку к менеджеру.
        """
        if self.manager is not None:
            raise ValidationError("Заявка уже закреплена за менеджером.")
        self.manager = manager
        self.save()

    def unassign_manager(self):
        """
        Убрать менеджера из заявки.
        """
        self.manager = None
        self.save()

    class Meta:
        verbose_name = 'Заявка на ипотеку'
        verbose_name_plural = 'Заявки на ипотеку'
