import datetime
from datetime import timezone
import uuid
import json
import requests
import datetime
import random
import string
import pyotp
import math
import stripe
import mimetypes
import base64
import io
import time
from PIL import Image

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from django.db.models import Q
from timezone_field import TimeZoneField
from store.models import FlexibleTicket
from orders.models import Purchase
from StreamStage.templatetags.tags import cross_app_reverse

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
    last_login = models.DateTimeField(auto_now=True)
    token = models.CharField("Token", max_length=100, blank=True, null=True)

    has_subscription = models.BooleanField("Has Subscription", default=False)
    subscription_id = models.CharField("Subscription ID", max_length=100, blank=True, null=True)
    subscription_start = models.IntegerField("Subscription Start", blank=True, null=True)
    subscription_end = models.IntegerField("Subscription End", blank=True, null=True)
    subscription_status = models.CharField("Subscription Status", max_length=100, default='none', blank=True, null=True)

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
                img = File(img_tmp, name=f'profile/pfp/{self.id}{image_ext}')
                self.profile_pic = img

            elif type == 'banner':
                img = File(img_tmp, name=f'profile/banners/{self.id}{image_ext}')
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
                img = File(img_tmp, name=f'profile/pfp/{uuid.uuid4()}.webp')
                self.profile_pic = img

            elif type == 'banner':
                img = File(img_tmp, name=f'profile/banners/{uuid.uuid4()}.webp')
                self.profile_banner = img

            self.save()
            return True

        except Exception as e:
            print(e)
            return False



    def is_subscribed(self):
        """
            Checks if a user is subscribed
            to a plan
        """

        subscribed = False
        WEEK = 604800 # -- 7 days in seconds floor(time.time() / 604800)
        now_plus_week = math.floor(time.time()) + WEEK
        end = self.subscription_end if self.subscription_end != None else 0


        if self.has_subscription == True: subscribed = True
        if end == None: subscribed = False
        if end < now_plus_week: subscribed = False
        

        if (
            self.subscription_status == "monthly" or
            self.subscription_status == "yearly" and
            end < now_plus_week
        ):
            """
                If the user has a subscription, and
                the subscription is still active
                Check if the user has paid for the
                subscription
            """

        return subscribed

        
    
    def serialize_subscription(self):
        """
            Serializes the subscription
            for the user
        """
        return {
            'has_subscription': self.has_subscription,
            'subscription_id': self.subscription_id,
            'subscription_start': self.subscription_start,
            'subscription_end': self.subscription_end,
            'subscription_status': self.subscription_status
        }
    


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
        try:
            customer = stripe.Customer.retrieve(self.stripe_customer)
            if customer: return customer
            return None
        
        except Exception as e:
            customer = stripe.Customer.create(
                email=self.email,
                name=self.username,
                description=self.id
            )
            self.stripe_customer = customer['id']
            self.save()
            return customer


    def set_plan(self, plan: str):
        """
            Sets the plan for a user
        """
        self.subscription_status = plan
        self.save()


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

    def get_authorized_broadcasters(self):
        return Broadcaster.objects.filter(Q(streamer = self) | Q(contributors__id=self.id))


    def get_tickets(self, expired: bool = True):
        """
            Returns all the tickets that belong to the user
            allows for a 24 hour grace period for expired tickets
        """
        purchases = Purchase.objects.filter(purchaser=self)
        tickets = []


        for purchase in purchases:
            pid = purchase.purchase_id
            pid_tickets = FlexibleTicket.objects.filter(purchase_id=pid).all()

            for ticket in pid_tickets.all():
                tickets.append(ticket)

        # -- Sort the tickets by date
        tickets_filtered = {
            'upcoming': [],
            'expired': [],
        }
        for ticket in tickets:
            # -- models.DateTimeField() to seconds
            event_start = ticket.listing.showing
            if event_start is None:
                tickets_filtered['upcoming'].append(ticket.serialize())
                continue
            event_start = event_start.time.timestamp()
            event_start += 86400 # -- Add 24 hours

            # -- Get the current time
            current_time = datetime.datetime.now(tz=timezone.utc)
            current_time = current_time.timestamp()

            # -- Check if the ticket is expired
            if event_start < current_time:
                if expired: tickets_filtered['expired'].append(ticket.serialize())
            else: tickets_filtered['upcoming'].append(ticket.serialize())


        return tickets_filtered


    def basic_serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'profile_pic': self.get_profile_pic(),
            'url': cross_app_reverse('homepage', 'user_profile', kwargs={'username': self.username}),
        }

    def set_username(self, username):
        """
            Sets the username of the user
        """
        username = username.strip()
        self.username = username.lower()
        self.cased_username = username
        self.save()
        self.ensure()

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

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField("Banner", upload_to="broadcaster", blank=True, null=True)
    profile_pic = models.ImageField("Profile Picture", upload_to="broadcaster", blank=True, null=True)
    
    
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



    def get_picture(self, type: str = 'profile_pic'):
        """
            Returns the a picture url based on the type
            - banner
            - profile_pic
        """
        if type == "banner":
            if self.banner is None or self.banner == "": 
                return None

            if self.banner is not None:
                return f'/{MEDIA_URL}{self.banner}'

        if type == "profile_pic":
            if self.profile_pic is None or self.profile_pic == "": 
                return '/static/images/placeholder-pfp.png'

            if self.profile_pic is not None:
                return f'/{MEDIA_URL}{self.profile_pic}'
            
        return None



    def set_picture_b64(self, type: str, base64_data: str):
        """
            Sets the picture based on a base64 string
            and of a certain type
            - banner
            - profile_pic
        """
        try:
            img_tmp = NamedTemporaryFile()
            image_data = base64.b64decode(base64_data.split(',')[1])
            image = Image.open(io.BytesIO(image_data))

            # -- Compress the image
            image = image.save(img_tmp, 'webp', quality=75)

            # -- Save the image to the media folder
            img_tmp.write(image_data)
            img_tmp.flush()

            # -- Set the image
            if type == "banner":
                img = File(img_tmp, name=f'banners/{uuid.uuid4()}.webp')
                self.banner = img

            elif type == "profile_pic":
                img = File(img_tmp, name=f'pfp/{uuid.uuid4()}.webp')
                self.profile_pic = img

            self.save()
            return True
        
        except Exception as e:
            print(e)
            return False
        

    def get_absolute_url(self):
        return cross_app_reverse('homepage', 'broadcaster_profile', {
            "username": self.handle
        })


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
    # r_broadcaster = models.ForeignKey('accounts.Broadcaster', on_delete=models.CASCADE, related_name="reported_broadcaster", null=True, blank=True)
    # r_review = models.ForeignKey('events.EventReview', on_delete=models.CASCADE, related_name="reported_review", null=True, blank=True)
    # r_event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name="reported_event", null=True, blank=True)

    reason = models.CharField("Reason", max_length=4000)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    solved = models.BooleanField("Solved", default=False)
    solved_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="solved_by", null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "reporter": self.reporter.basic_serialize(),
            "reason": self.reason,
            "time": self.time,
            "date": self.date,
            "reported": {
                "user": self.r_user.basic_serialize(),
                # "broadcaster": self.r_broadcaster,
                # "review": self.r_review,
                # "event": self.r_event,
            },
            "solved": self.solved,
            "reported_fields": {
                "user": True if self.r_user is not None else False,
                # "broadcaster": True if self.r_broadcaster is not None else False,
                # "review": True if self.r_review is not None else False,
                # "event": True if self.r_event is not None else False,
            },
            "solved_by": self.solved_by.basic_serialize() if self.solved_by is not None else None,
            "created": self.created,
            "updated": self.updated,
        }

class BroadcasterContributeInvite(models.Model):
    broadcaster = models.ForeignKey(Broadcaster, on_delete=models.CASCADE, related_name="broadcaster")
    inviter = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="inviter")
    invitee = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="invitee")
    
    message = models.TextField(max_length=256)

    is_pending = models.BooleanField("Is Pending", default=True)

