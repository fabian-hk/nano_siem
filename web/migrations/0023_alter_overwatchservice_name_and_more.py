# Generated by Django 4.1.3 on 2023-01-30 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0022_rename_notify_overwatchservice_notified"),
    ]

    operations = [
        migrations.AlterField(
            model_name="overwatchservice",
            name="name",
            field=models.TextField(),
        ),
        migrations.AlterUniqueTogether(
            name="overwatchservice",
            unique_together={("name", "type")},
        ),
    ]