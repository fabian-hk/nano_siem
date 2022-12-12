# Generated by Django 4.1.3 on 2022-12-10 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0014_alter_servicelogfail_seen"),
    ]

    operations = [
        migrations.AddField(
            model_name="servicelogfail",
            name="autonomous_system_organization",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="servicelogfail",
            name="city_name",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="servicelogfail",
            name="country_name",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="servicelogfail",
            name="is_tor",
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name="servicelogfail",
            name="latitude",
            field=models.FloatField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="servicelogfail",
            name="longitude",
            field=models.FloatField(db_index=True, null=True),
        ),
    ]