# Generated by Django 2.0.3 on 2018-04-30 11:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blabla', '0002_auto_20180423_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
