# Generated by Django 4.1.5 on 2023-02-01 13:36

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('server_manager', '0009_publisher_ingest_server_alter_server_mode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamaccess',
            name='key',
            field=models.CharField(default='9be14db5dcd840af8a8ea8d3791772cd', max_length=64, validators=[django.core.validators.MinLengthValidator(32)]),
        ),
        migrations.RemoveField(
            model_name='streamaccess',
            name='member',
        ),
        migrations.AddField(
            model_name='streamaccess',
            name='member',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
