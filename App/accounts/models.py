import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from timezone_field import TimeZoneField

from .oauth import OAuthTypes


# Create your models here.
class Member(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField("Username", max_length=30, unique=True)
    cased_username = models.CharField("Cased Username", max_length=30, unique=True)
    email = models.EmailField("Email", unique=True)
    date_of_birth = models.DateField(default=None, null=True)
    over_18 = models.BooleanField(default=False)
    profile_pic = models.ImageField("Profile Photo", upload_to='member', blank=True)
    description = models.TextField("Description", blank=True)
    country = CountryField()
    time_zone = TimeZoneField(default="UTC")

    # Access Level for member. 0 for basic. See list of access level codes for other levels.
    access_level = models.SmallIntegerField("Access Level", default=0)
    # Maximum parallel devices for a Member to watch on
    max_keys = models.SmallIntegerField("Max Devices", default=1)
    # 
    is_streamer = models.BooleanField("Streamer Status", default=False)
    is_broadcaster = models.BooleanField("Broadcaster Status", default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
      return str(self.username)

    def mask_email(self):
        keep = 2
        email = self.email.split('@')

        # If the first part of the email is less than 3 characters, return the email
        if len(email[0]) < keep:
            return "****@" + email[1]

        # keep x from the start and the end
        return email[0][:keep] + "****" + email[0][-keep:] + "@" + email[1]

    def is_over_18(self):
        import datetime
        if (self.date_of_birth == None):
            self.over_18 = False
        elif (datetime.date.today() - self.date_of_birth) > datetime.timedelta(days=18*365):
            self.over_18 = True

    def save(self, *args, **kwargs):
        self.is_over_18()
        self.cased_username = self.username.lower()
        super(Member, self).save(*args, **kwargs)

# Broadcaster - entity that controls events/streams
class Broadcaster(models.Model):
    # Streamer who creates events/streams and invites contributors to broadcast event
    streamer = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True
    )
    # Members who can control a broadcast
    contributors = models.ManyToManyField(get_user_model(), related_name="stream_broadcasters", blank=True)
    # Categories of streaming content
    category = models.CharField("Categories", max_length=100)
    approved = models.BooleanField("Approved", default=False)

    USERNAME_FIELD = 'streamer'
    REQUIRED_FIELDS = ['category']

    def __str__(self):
        return str(self.user)


class oAuth2(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    oauth_type = models.SmallIntegerField("Type", choices=OAuthTypes.choices)
    oauth_id = models.CharField("OAuth ID", max_length=100, unique=True)
    
class TwoFactorAuth(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    secret = models.CharField("Secret", max_length=100)
