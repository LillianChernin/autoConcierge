# Generated by Django 2.0.2 on 2018-03-01 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_auto_20180301_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopowner',
            name='address_gps_lat',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='shopowner',
            name='address_gps_lng',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=10),
        ),
    ]