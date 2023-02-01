# Generated by Django 4.1.5 on 2023-01-30 13:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server_manager', '0008_publisher_server_list_alter_streamaccess_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisher',
            name='ingest_server',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ingest_server', to='server_manager.server'),
        ),
        migrations.AlterField(
            model_name='server',
            name='mode',
            field=models.CharField(choices=[('I', 'Ingest'), ('R', 'Relay'), ('RR', 'Root Relay')], default='I', max_length=2),
        ),
        migrations.AlterField(
            model_name='streamaccess',
            name='key',
            field=models.CharField(default='e5cedc75399ec7c6fc9112777a7e1dfa', max_length=64, validators=[django.core.validators.MinLengthValidator(32)]),
        ),
    ]