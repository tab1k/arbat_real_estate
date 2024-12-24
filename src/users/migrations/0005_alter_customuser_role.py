# Generated by Django 5.1.4 on 2024-12-24 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_customuser_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="role",
            field=models.CharField(
                choices=[
                    ("admin", "Администратор"),
                    ("manager", "Менеджер"),
                    ("user", "Пользователь"),
                ],
                max_length=255,
            ),
        ),
    ]