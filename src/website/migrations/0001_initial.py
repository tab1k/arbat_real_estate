# Generated by Django 5.1.4 on 2024-12-24 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CreepingLine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="creeping_lines/", verbose_name="Изображение"
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=155, verbose_name="Название линии"),
                ),
                ("text", models.TextField(max_length=100, verbose_name="Текст")),
            ],
            options={
                "verbose_name": "Бегающая линия",
                "verbose_name_plural": "Бегающая линия",
            },
        ),
        migrations.CreateModel(
            name="ExclusiveOffer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="exclusive_offers/", verbose_name="Изображение"
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Название ЖК")),
                (
                    "city",
                    models.CharField(
                        choices=[
                            ("tse", "Астана"),
                            ("ala", "Алматы"),
                            ("shy", "Шымкент"),
                            ("akt", "Актобе"),
                            ("aty", "Атырау"),
                            ("ktb", "Караганда"),
                            ("kst", "Костанай"),
                            ("kzo", "Кызылорда"),
                            ("aktk", "Актау"),
                            ("tar", "Тараз"),
                            ("urk", "Уральск"),
                            ("osk", "Усть-Каменогорск"),
                            ("sem", "Семей"),
                            ("pet", "Петропавловск"),
                            ("tem", "Темиртау"),
                            ("ekt", "Экибастуз"),
                        ],
                        max_length=255,
                        verbose_name="Город",
                    ),
                ),
                ("side", models.CharField(max_length=255, verbose_name="Район")),
                ("area", models.CharField(max_length=255, verbose_name="Площадь")),
                ("rooms", models.PositiveIntegerField(verbose_name="Комнат")),
                ("mark", models.PositiveIntegerField(verbose_name="Звезд")),
                ("price", models.PositiveBigIntegerField(verbose_name="Цена")),
            ],
            options={
                "verbose_name": "Эксклюзивное предложение",
                "verbose_name_plural": "Эксклюзивные предложения",
            },
        ),
    ]