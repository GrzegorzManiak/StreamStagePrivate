# Generated by Django 4.1.7 on 2023-02-28 21:58

import accounts.validation
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import timezone_field.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Username')),
                ('cased_username', models.CharField(max_length=30, unique=True, verbose_name='Cased Username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('date_of_birth', models.DateField(default=None, null=True)),
                ('over_18', models.BooleanField(default=False)),
                ('profile_pic', models.ImageField(blank=True, upload_to='member', verbose_name='Profile Photo')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('time_zone', timezone_field.fields.TimeZoneField(default='UTC')),
                ('tfa_secret', models.CharField(blank=True, max_length=100, null=True, verbose_name='tfa_secret')),
                ('access_level', models.SmallIntegerField(default=0, verbose_name='Access Level')),
                ('max_keys', models.SmallIntegerField(default=1, verbose_name='Max Devices')),
                ('is_streamer', models.BooleanField(default=False, verbose_name='Streamer Status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='oAuth2',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('oauth_type', models.SmallIntegerField(choices=[(0, 'Google'), (1, 'Discord'), (2, 'Github')], verbose_name='Type')),
                ('oauth_id', models.CharField(max_length=100, unique=True, verbose_name='OAuth ID')),
                ('last_used', models.DateTimeField(auto_now=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoginHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ip', models.GenericIPAddressField(protocol='IPv4', verbose_name='IP Address')),
                ('time', models.TimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('method', models.CharField(max_length=64, verbose_name='Method')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Broadcaster',
            fields=[
                ('handle', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, validators=[accounts.validation.check_unique_broadcaster_handle], verbose_name='Broadcaster Handle')),
                ('name', models.CharField(max_length=32, verbose_name='name')),
                ('biography', models.TextField(max_length=512, verbose_name='Biography')),
                ('over_18', models.BooleanField()),
                ('approved', models.BooleanField(default=False, verbose_name='Approved')),
                ('contributors', models.ManyToManyField(blank=True, related_name='stream_broadcasters', to=settings.AUTH_USER_MODEL)),
                ('streamer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
