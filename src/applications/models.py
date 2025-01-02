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

    realtor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')

    full_name = models.CharField(max_length=255)
    iin = models.PositiveBigIntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=25)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    down_payment = models.DecimalField(max_digits=12, decimal_places=2)
    mortgage_term = models.IntegerField()
    city = models.CharField(max_length=100)

    status = models.CharField(choices=STATUS_CHOICES, blank=True, max_length=50, default='in_work')

    code = models.CharField(max_length=10, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заявка от {self.full_name} ({self.phone_number})'

    class Meta:
        verbose_name = 'Заявка на ипотеку'
        verbose_name_plural = 'Заявки на ипотеку'
