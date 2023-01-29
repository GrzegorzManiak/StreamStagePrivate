from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
import uuid

# Create your models here.
class Member(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField("Username", max_length=25, unique=True, null=False, blank=False)
    access_level = models.PositiveBigIntegerField("Access Level", null=False, blank=False)



class StreamerProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        null=False,
        on_delete=models.CASCADE,
        primary_key=True
    )
    
    category = models.CharField("Category", max_length=50, null=False, blank=False)
    

    def __str__(self):
        return str(self.member)