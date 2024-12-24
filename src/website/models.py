from django.db import models
from django.utils import timezone


class CreepingLine(models.Model):
    image = models.ImageField(upload_to='creeping_lines/', verbose_name='Изображение')
    title = models.CharField(max_length=155, blank=False, verbose_name='Название линии')
    text = models.TextField(max_length=100, blank=False, verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Бегающая линия'
        verbose_name_plural = 'Бегающая линия'


class ExclusiveOffer(models.Model):
    CITY_CHOICES = (
        ('tse', 'Астана'),
        ('ala', 'Алматы'),
        ('shy', 'Шымкент'),
        ('akt', 'Актобе'),
        ('aty', 'Атырау'),
        ('ktb', 'Караганда'),
        ('kst', 'Костанай'),
        ('kzo', 'Кызылорда'),
        ('aktk', 'Актау'),
        ('tar', 'Тараз'),
        ('urk', 'Уральск'),
        ('osk', 'Усть-Каменогорск'),
        ('sem', 'Семей'),
        ('pet', 'Петропавловск'),
        ('tem', 'Темиртау'),
        ('ekt', 'Экибастуз'),
    )

    image = models.ImageField(upload_to='exclusive_offers/', blank=False, verbose_name='Изображение')

    name = models.CharField(max_length=255, blank=False, verbose_name='Название ЖК')
    city = models.CharField(max_length=255, choices=CITY_CHOICES, verbose_name='Город')
    side = models.CharField(max_length=255, blank=False, verbose_name='Район')
    area = models.CharField(max_length=255, blank=False, verbose_name='Площадь')
    rooms = models.PositiveIntegerField(blank=False, verbose_name='Комнат')
    mark = models.PositiveIntegerField(blank=False, verbose_name='Звезд')
    price = models.PositiveBigIntegerField(blank=False, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Дата создания')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Эксклюзивное предложение'
        verbose_name_plural = 'Эксклюзивные предложения'
