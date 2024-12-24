import re
from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError



class CustomUser(AbstractUser):

    USER_ROLES = (
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('user', 'Пользователь'),
    )

    username = None  # Удаляем стандартное поле username
    phone_number = models.CharField(
        max_length=25,
        unique=True,
        verbose_name="Номер телефона"
    )
    email = models.EmailField(blank=True)
    date_of_birth = models.DateField(
        verbose_name="Дата рождения",
        blank=True,
        null=True,
    )

    photo = models.ImageField(upload_to='user_photos/', blank=True, verbose_name="Фотография")

    role = models.CharField(choices=USER_ROLES, blank=False, max_length=255)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}' or self.phone_number

    def clean(self):
        super().clean()
        if not self.phone_number:
            raise ValidationError("Номер телефона не может быть пустым.")
        # Убедитесь, что номер начинается с +7
        if not self.phone_number.startswith('+7'):
            self.phone_number = '+7' + self.phone_number.lstrip('+7')
        # Убедитесь, что номер состоит только из цифр после +7
        if not re.match(r'^\+7[0-9]+$', self.phone_number):
            raise ValidationError("Номер телефона должен состоять из цифр.")

    def save(self, *args, **kwargs):
        # Форматирование номера телефона
        if not self.phone_number.startswith('+7'):
            self.phone_number = '+7' + self.phone_number.lstrip('+7')
        self.phone_number = re.sub(r'[^0-9+]', '', self.phone_number)
        super().save(*args, **kwargs)


