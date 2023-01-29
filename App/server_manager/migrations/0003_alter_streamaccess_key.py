# Generated by Django 3.2.16 on 2023-01-29 16:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_manager', '0002_alter_streamaccess_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamaccess',
            name='key',
            field=models.CharField(default='67a2c0f8f62dbd8f6d8c7cd81cd4340d', max_length=64, validators=[django.core.validators.MinLengthValidator(32)]),
        ),
    ]
