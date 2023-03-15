import uuid
import requests

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from timezone_field import TimeZoneField

from .oauth import OAuthTypes
import stripe

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from .validation import check_unique_broadcaster_handle

from StreamStage.secrets import STRIPE_SECRET_KEY

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
    stripe_customer = models.CharField("Stripe Customer ID", max_length=100, blank=True)
    country = CountryField()
    time_zone = TimeZoneField(default="UTC")
    tfa_secret = models.CharField(
        "tfa_secret", 
        max_length=100,
        blank=True,
        null=True,
    )

    # Access Level for member. 0 for basic. See list of access level codes for other levels.
    access_level = models.SmallIntegerField("Access Level", default=0)
    # Maximum parallel devices for a Member to watch on
    max_keys = models.SmallIntegerField("Max Devices", default=1)
    # Is Member more than a basic member?
    is_streamer = models.BooleanField("Streamer Status", default=False)

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

    def add_profile_pic_from_url(self, url):
        try:
            img_tmp = NamedTemporaryFile(delete=True)
            img_content = requests.get(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
                }
            ).content

            img_tmp.write(img_content)
            img_tmp.flush()
            
            img = File(img_tmp, name=f'profile_pictures/{self.id}.jpg')
            self.profile_pic = img

            self.save()

        
        except Exception as e:
            print(e)
            return False
        
    def get_stripe_customer(self):
        stripe.api_key = STRIPE_SECRET_KEY

        # -- Check if the user has a stripe customer id
        if self.stripe_customer == "":
            customer = stripe.Customer.create(
                email=self.email,
                name=self.username,
                description=self.id
            )
            self.stripe_customer = customer['id']
            self.save()
            return customer
        
        # -- If the user has a stripe customer id, return the customer
        customer = stripe.Customer.retrieve(self.stripe_customer)
        if customer: return customer
        return None
    

    def save(self, *args, **kwargs):
        self.is_over_18()
        self.cased_username = self.username.lower()

        super(Member, self).save(*args, **kwargs)

        

# Broadcaster - entity that controls events/streams
class Broadcaster(models.Model):
    handle = models.CharField("Broadcaster Handle", unique=True, primary_key=True, max_length=20, validators=[ check_unique_broadcaster_handle ])
    # Streamer who creates events/streams and invites contributors to broadcast event
    streamer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=False
    )
    # Members who can control a broadcast
    contributors = models.ManyToManyField(get_user_model(), related_name="stream_broadcasters", blank=True)
    # Categories of streaming content
    #category = models.ManyToManyField("events.Category", verbose_name="Categories")
    
    name = models.CharField("name", max_length=32)
    biography = models.TextField("Biography", max_length=512)

    # Should we hide this entire broadcaster from minor members?
    over_18 = models.BooleanField()

    # whether the application for this broadcaster has been approved
    approved = models.BooleanField("Approved", default=False)
    
    USERNAME_FIELD = 'streamer'
    REQUIRED_FIELDS = ['category']

    def __str__(self):
        return str("@" + self.handle)


class oAuth2(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    oauth_type = models.SmallIntegerField("Type", choices=OAuthTypes.choices)
    oauth_id = models.CharField("OAuth ID", max_length=100, unique=True)

    last_used = models.DateTimeField(auto_now=True)
    added = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "oauth_type": self.oauth_type,
            "oauth_id": self.oauth_id,
            "last_used": self.last_used,
            "added": self.added,
        }


class LoginHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    ip = models.GenericIPAddressField("IP Address", protocol='IPv4')
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    method = models.CharField("Method", max_length=64)

    def serialize(self):
        return {
            "id": self.id,
            "ip": self.ip,
            "time": self.time,
            "date": self.date,
            "method": self.method,
        }
    

