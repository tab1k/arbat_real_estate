# Generated by Django 5.1.4 on 2025-01-01 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0005_alter_mortgageapplication_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="mortgageapplication",
            name="code",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
