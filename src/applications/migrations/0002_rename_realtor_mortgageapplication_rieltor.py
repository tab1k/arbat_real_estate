# Generated by Django 5.1.4 on 2025-01-01 01:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="mortgageapplication",
            old_name="realtor",
            new_name="rieltor",
        ),
    ]
