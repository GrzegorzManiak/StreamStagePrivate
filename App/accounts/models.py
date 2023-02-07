from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from .oauth.oauth import OAuthTypes
import uuid


# Create your models here.
class Member(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField("Username", max_length=30, unique=True)
    email = models.EmailField("Email", unique=True)
    profile_pic = models.ImageField("Profile Photo", upload_to='member', blank=True)
    description = models.TextField("Description", blank=True)

    # Access Level for member. 0 for basic. See list of access level codes for other levels.
    access_level = models.SmallIntegerField("Access Level", default=0)
    # Maximum parallel devices for a Member to watch on
    max_keys = models.SmallIntegerField("Max Devices", default=1)
    
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





class StreamerProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True
    )
    # Categories of streaming content
    category = models.CharField("Categories", max_length=100)

    USERNAME_FIELD = 'username'
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
