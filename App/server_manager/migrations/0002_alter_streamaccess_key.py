# Generated by Django 4.1.5 on 2023-01-27 14:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamaccess',
            name='key',
            field=models.CharField(default='16ece7d259da332752a3ad28be4bc969', max_length=64, validators=[django.core.validators.MinLengthValidator(32)]),
        ),
    ]