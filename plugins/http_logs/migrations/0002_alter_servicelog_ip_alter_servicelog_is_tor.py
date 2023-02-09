# Generated by Django 4.1.3 on 2023-02-08 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("http_logs", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="servicelog",
            name="ip",
            field=models.GenericIPAddressField(db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="servicelog",
            name="is_tor",
            field=models.BooleanField(db_index=True, null=True),
        ),
    ]