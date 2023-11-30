# Generated by Django 4.2.7 on 2023-11-26 12:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("overwatch", "0003_remove_diskservice_available_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="diskservice",
            old_name="last_available",
            new_name="unavailable_since",
        ),
        migrations.RenameField(
            model_name="networkservice",
            old_name="last_available",
            new_name="unavailable_since",
        ),
    ]