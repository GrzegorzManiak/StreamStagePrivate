import datetime
from datetime import timezone
import uuid
import json
import requests
import datetime
import random
import string
import pyotp
import stripe
import mimetypes
import base64
import io
from PIL import Image

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from timezone_field import TimeZoneField

from .oauth import OAuthTypes

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from .validation import check_unique_broadcaster_handle

from StreamStage.secrets import STRIPE_SECRET_KEY
from StreamStage.settings import MEDIA_URL
from StreamStage.mail import send_template_email
stripe.api_key = STRIPE_SECRET_KEY

class SecurityPreferences(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email_on_login           = models.BooleanField('Email on Login',           default=True, 
        help_text="Send an email when you log in from a new device")
    email_on_password_change = models.BooleanField('Email on Password Change', default=True,
        help_text="Send an email when you change your password")    
    email_on_email_change    = models.BooleanField('Email on Email Change',    default=True,
        help_text="Send an email when you change your email address")
    email_on_password_reset  = models.BooleanField('Email on Password Reset',  default=True,
        help_text="Send an email when you reset your password")
    email_on_oauth_change    = models.BooleanField('Email on OAuth Change',    default=True,
        help_text="Send an email when you add or remove an OAuth provider")
    email_on_payment_change  = models.BooleanField('Email on Payment Change',  default=True,
        help_text="Send an email when you add or remove a payment method")
    email_on_subscription_change = models.BooleanField('Email on Subscription Change', default=True,
        help_text="Send an email when you add or remove a subscription")
    email_on_mfa_change      = models.BooleanField('Email on MFA Change',      default=True,
        help_text="Send an email when you add or remove MFA")
    email_on_purchases       = models.BooleanField('Email on Purchases',       default=True,
        help_text="Send an email when you make a purchase")                                        
    require_mfa_on_login     = models.BooleanField('Require MFA on Login',     default=False,
        help_text="Require MFA when you log in")
    require_mfa_on_payment   = models.BooleanField('Require MFA on Payment',   default=False,
        help_text="Require MFA when you make a payment")
    public_profile           = models.BooleanField('Public Profile',           default=True,
        help_text="Make your profile public")
    public_name              = models.BooleanField('Public Name',              default=False,
        help_text="Makes your full name public on your profile")
    public_country           = models.BooleanField('Public Country',           default=False,
        help_text="Makes your country public on your profile")

    
    def get_keys(self):
        return [f.name for f in self._meta.get_fields()]
    
    def set(self, key, value):
        if (key == 'id'): return
        if (key not in self.get_keys()): return

        setattr(self, key, value)
        self.save()
    
    def serialize(self):
        # Gets all the fields of the model and returns them as a dictionary
        # { key: value, name: value, help_text: value }
        formated = {}

        for key in self.get_keys():
            if (key == 'id' or key == 'member'): continue
            field = self._meta.get_field(key)

            formated[key] = {
                'value': getattr(self, key),
                'name': field.__dict__.get('verbose_name'),
                'help_text': field.__dict__.get('help_text')
            }
    
        return formated
    

# Create your models here.
class Member(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField("Username", max_length=30, unique=True)
    cased_username = models.CharField("Cased Username", max_length=30, unique=True)
    email = models.EmailField("Email", unique=True)
    date_of_birth = models.DateField(default=None, null=True)
    over_18 = models.BooleanField(default=False)
    profile_pic = models.ImageField("Profile Photo", upload_to='member', blank=True)
    profile_banner = models.ImageField("Profile Banner", upload_to='member', blank=True)
    description = models.TextField("Description", blank=True)
    stripe_customer = models.CharField("Stripe Customer ID", max_length=100, blank=True)
    security_preferences = models.OneToOneField(SecurityPreferences, on_delete=models.CASCADE, null=True, blank=True)
    country = CountryField(default='Ireland')
    time_zone = TimeZoneField(default="Europe/Dublin")
    tfa_secret = models.CharField("tfa_secret", max_length=100, blank=True, null=True)
    tfa_recovery_codes = models.TextField("tfa_recovery_codes", blank=True, null=True)
    access_level = models.SmallIntegerField("Access Level", default=0)
    max_keys = models.SmallIntegerField("Max Devices", default=1)
    is_streamer = models.BooleanField("Streamer Status", default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
      return str(self.username)


    def mask_email(self, keep: int = 2):
        """
            Masks an email address, keeping
            the first x characters and the last
            x characters
        """
        email = self.email.split('@')
        if len(email[0]) < keep:
            return "****@" + email[1]
        return email[0][:keep] + "****" + email[0][-keep:] + "@" + email[1]



    def is_over_18(self):
        """
            Checks if a user is over 18, sets a flag
            if so
        """
        if (self.date_of_birth == None): self.over_18 = False
        elif (datetime.date.today() - self.date_of_birth) > datetime.timedelta(days=18*365):
            self.over_18 = True



    def add_pic_from_url(self, url: str, type: str):
        """
            Adds a profile picture to a user
            from a url, and saves it to the
            media folder
        """
        try:
            img_tmp = NamedTemporaryFile(delete=True)
            img_content = requests.get(
                url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
                }
            )
            
            image_type = img_content.headers['Content-Type'] # -- Mime type
            image_ext = mimetypes.guess_extension(image_type) # -- File extension

            if image_ext == None: return False            
            
            img_tmp.write(img_content.content)
            img_tmp.flush()   
            
            if type == 'pfp':
                img = File(img_tmp, name=f'profile_pictures/{self.id}{image_ext}')
                self.profile_pic = img

            elif type == 'banner':
                img = File(img_tmp, name=f'profile_banners/{self.id}{image_ext}')
                self.profile_banner = img

            self.save()
        
        except Exception as e: return False
        

    def add_pic_from_base64(self, base64_data: str, type: str):
        """
            Adds a profile picture to a user
            from a base64 string, and saves it
            to the media folder
        """
        try:
            img_tmp = NamedTemporaryFile(delete=True)
            image_data = base64.b64decode(base64_data.split(',')[1])
            image = Image.open(io.BytesIO(image_data))

            # -- Compress the image
            image = image.save(img_tmp, 'webp', quality=75)

            # -- Save the image to the media folder
            img_tmp.write(image_data)
            img_tmp.flush()

            if type == 'pfp':
                img = File(img_tmp, name=f'profile_pictures/{uuid.uuid4()}.webp')
                self.profile_pic = img

            elif type == 'banner':
                img = File(img_tmp, name=f'profile_banners/{uuid.uuid4()}.webp')
                self.profile_banner = img

            self.save()
            return True

        except Exception as e:
            print(e)
            return False



    def get_stripe_customer(self):
        """
            Gets the stripe customer id for a
            given user, and creates it if 
            the user doesn't have one
        """

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



    def set_recovery_codes(self):
        """
            Generates 6 Alpha-Numeric recovery
            codes and saves them to the user
        """
        codes = []
        for _i in range(6):
            codes.append(''.join(random.choices(string.ascii_letters + string.digits, k=6)))
        self.tfa_recovery_codes = json.dumps(codes)
        self.save()



    def get_recovery_codes(self):
        """
            Returns the recovery codes as a list
        """
        if self.tfa_recovery_codes == None: return None
        return json.loads(self.tfa_recovery_codes)
    


    def remove_recovery_code(self, code: str):
        """
            Removes a recovery code from the user
            when the user uses it.
        """
        codes = self.get_recovery_codes()
        codes.remove(code)
        self.tfa_recovery_codes = json.dumps(codes)
        self.save()
    


    def verify_mfa(self, code: str):
        """
            Verify the code given by the user,
            it also checks if the code is a
            recovery code, if it is, it removes
            the recovery code from the user.
        """
        # -- Check if the user has a tfa secret
        if self.tfa_secret == None: return False

        # -- Get the recovery codes
        recovery_codes = self.get_recovery_codes()
        for recovery_code in recovery_codes:
            if recovery_code != code: break
            
            # -- Remove the recovery code
            self.remove_recovery_code(recovery_code)
            codes_left = len(self.get_recovery_codes())
            if self.security_preferences.email_on_mfa_change:
                send_template_email(self, 'mfa_recovery', codes_left)

            return True
        
        # -- Verify the code
        return pyotp.TOTP(self.tfa_secret).verify(code)



    def default_profile_pic(self):
        url = f'https://api.dicebear.com/5.x/thumbs/svg?seed={self.id}'
        return self.add_pic_from_url(url, 'pfp')

    def default_profile_banner(self):
        url = f'https://api.dicebear.com/5.x/thumbs/svg?seed={self.id}'
        return self.add_pic_from_url(url, 'banner')


    def get_profile_pic(self):
        """
            Returns the profile picture url
        """
        if self.profile_pic is None or self.profile_pic == "": 
            self.default_profile_pic()

        if self.profile_pic is not None:
            return f'/{MEDIA_URL}{self.profile_pic}'


    def get_profile_banner(self):
        """
            Returns the profile banner url
        """
        if self.profile_banner is None or self.profile_banner == "": 
            return self.default_profile_banner()

        if self.profile_banner is not None:
            return f'/{MEDIA_URL}{self.profile_banner}'



    def ensure(self, *args, **kwargs):
        # -- Check if the account has been created

        # -- Check if we have a security preferences object
        if self.security_preferences is None:
            self.security_preferences = SecurityPreferences.objects.create()
            
        self.is_over_18()
        
        # -- Make sure we have a cased username
        if self.username != self.cased_username.lower():
            self.cased_username = self.username.lower()

        # -- Check if the user has a profile picture
        if self.profile_pic is None or self.profile_pic == "":
            self.default_profile_pic()

        # -- Check if the user has a profile banner\
        if self.profile_banner is None or self.profile_banner == "":
            self.default_profile_banner()

        # -- Save the user
        self.save()



class MembershipStatus(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    expires_on = models.DateTimeField("Membership Expiration Date", blank=True)
    
    def is_valid(self):
        return self.get_remaining_time().total_seconds() > 0
    
    def get_remaining_time(self):
        return (self.expires_on.astimezone(timezone.utc) - datetime.datetime.now(tz=timezone.utc))
    
# Broadcaster - entity that controls events/streams
class Broadcaster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    handle = models.CharField("Broadcaster Handle", unique=True, max_length=20, validators=[ check_unique_broadcaster_handle ])

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

    def change_handle(self, new_handle):
        """
            Simply updates the handle of the broadcaster.
        """
        self.handle = new_handle.lower()
        self.save()

        


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


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reporter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="reporter")
        
    r_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="reported_user", null=True, blank=True)

    reason = models.CharField("Reason", max_length=4000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "reporter": self.reporter,
            "reported": self.reported,
            "reason": self.reason,
            "time": self.time,
            "date": self.date,
        }