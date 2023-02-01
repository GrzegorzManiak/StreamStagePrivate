# Generated by Django 4.1.5 on 2023-02-01 13:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('server_manager', '0010_alter_streamaccess_key_remove_streamaccess_member_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamaccess',
            name='key',
            field=models.CharField(default='4a9fb9809d95e60784f28f368667d8d8', max_length=64, validators=[django.core.validators.MinLengthValidator(32)]),
        ),
        migrations.RemoveField(
            model_name='streamaccess',
            name='member',
        ),
        migrations.AddField(
            model_name='streamaccess',
            name='member',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
