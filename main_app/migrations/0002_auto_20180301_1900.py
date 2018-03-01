# Generated by Django 2.0.2 on 2018-03-01 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='owner_id',
        ),
        migrations.AddField(
            model_name='car',
            name='car_license',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='car',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='car_owner', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]