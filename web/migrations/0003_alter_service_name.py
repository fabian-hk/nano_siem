# Generated by Django 4.1.3 on 2022-11-21 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_rename_asn_servicelog_autonomous_system_organization_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.TextField(unique=True),
        ),
    ]
