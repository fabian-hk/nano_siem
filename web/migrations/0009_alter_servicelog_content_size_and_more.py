# Generated by Django 4.1.3 on 2022-11-24 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_alter_servicelog_latitude_alter_servicelog_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicelog',
            name='content_size',
            field=models.PositiveBigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='servicelog',
            name='http_status',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
