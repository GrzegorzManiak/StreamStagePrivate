# Generated by Django 4.1.1 on 2023-04-02 14:42

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
                ('profile_banner', models.ImageField(blank=True, upload_to='member', verbose_name='Profile Banner')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('stripe_customer', models.CharField(blank=True, max_length=100, verbose_name='Stripe Customer ID')),
                ('country', django_countries.fields.CountryField(default='Ireland', max_length=2)),
                ('time_zone', timezone_field.fields.TimeZoneField(default='Europe/Dublin')),
                ('tfa_secret', models.CharField(blank=True, max_length=100, null=True, verbose_name='tfa_secret')),
                ('tfa_recovery_codes', models.TextField(blank=True, null=True, verbose_name='tfa_recovery_codes')),
                ('access_level', models.SmallIntegerField(default=0, verbose_name='Access Level')),
                ('max_keys', models.SmallIntegerField(default=1, verbose_name='Max Devices')),
                ('is_streamer', models.BooleanField(default=False, verbose_name='Streamer Status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
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
            name='SecurityPreferences',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email_on_login', models.BooleanField(default=True, help_text='Send an email when you log in from a new device', verbose_name='Email on Login')),
                ('email_on_password_change', models.BooleanField(default=True, help_text='Send an email when you change your password', verbose_name='Email on Password Change')),
                ('email_on_email_change', models.BooleanField(default=True, help_text='Send an email when you change your email address', verbose_name='Email on Email Change')),
                ('email_on_password_reset', models.BooleanField(default=True, help_text='Send an email when you reset your password', verbose_name='Email on Password Reset')),
                ('email_on_oauth_change', models.BooleanField(default=True, help_text='Send an email when you add or remove an OAuth provider', verbose_name='Email on OAuth Change')),
                ('email_on_payment_change', models.BooleanField(default=True, help_text='Send an email when you add or remove a payment method', verbose_name='Email on Payment Change')),
                ('email_on_subscription_change', models.BooleanField(default=True, help_text='Send an email when you add or remove a subscription', verbose_name='Email on Subscription Change')),
                ('email_on_mfa_change', models.BooleanField(default=True, help_text='Send an email when you add or remove MFA', verbose_name='Email on MFA Change')),
                ('email_on_purchases', models.BooleanField(default=True, help_text='Send an email when you make a purchase', verbose_name='Email on Purchases')),
                ('require_mfa_on_login', models.BooleanField(default=False, help_text='Require MFA when you log in', verbose_name='Require MFA on Login')),
                ('require_mfa_on_payment', models.BooleanField(default=False, help_text='Require MFA when you make a payment', verbose_name='Require MFA on Payment')),
                ('public_profile', models.BooleanField(default=True, help_text='Make your profile public', verbose_name='Public Profile')),
                ('public_name', models.BooleanField(default=False, help_text='Makes your full name public on your profile', verbose_name='Public Name')),
                ('public_country', models.BooleanField(default=False, help_text='Makes your country public on your profile', verbose_name='Public Country')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reason', models.CharField(max_length=4000, verbose_name='Reason')),
                ('time', models.TimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('r_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reported_user', to=settings.AUTH_USER_MODEL)),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporter', to=settings.AUTH_USER_MODEL)),
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
            name='MembershipStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expires_on', models.DateTimeField(blank=True, verbose_name='Membership Expiration Date')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('handle', models.CharField(max_length=20, unique=True, validators=[accounts.validation.check_unique_broadcaster_handle], verbose_name='Broadcaster Handle')),
                ('name', models.CharField(max_length=32, verbose_name='name')),
                ('biography', models.TextField(max_length=512, verbose_name='Biography')),
                ('over_18', models.BooleanField()),
                ('approved', models.BooleanField(default=False, verbose_name='Approved')),
                ('contributors', models.ManyToManyField(blank=True, related_name='stream_broadcasters', to=settings.AUTH_USER_MODEL)),
                ('streamer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='security_preferences',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.securitypreferences'),
        ),
        migrations.AddField(
            model_name='member',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
