# Generated by Django 4.1.3 on 2022-11-21 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_alter_service_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='modification_time',
            field=models.DateField(auto_now=True),
        ),
    ]
