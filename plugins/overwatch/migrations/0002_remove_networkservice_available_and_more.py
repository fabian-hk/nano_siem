# Generated by Django 4.2.7 on 2023-11-25 18:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("overwatch", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="networkservice",
            name="available",
        ),
        migrations.AddField(
            model_name="networkservice",
            name="last_available",
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
