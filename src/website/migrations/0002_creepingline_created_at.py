# Generated by Django 5.1.4 on 2024-12-24 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="creepingline",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
    ]