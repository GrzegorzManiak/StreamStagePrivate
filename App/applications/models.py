from django.db import models
from ..accounts.models import Member
from ..events.models import Event

# Create your models here.

class StreamerApplication(models.Model):
    applicant = models.ForeignKey(Member)
    event = models.ForeignKey(Event)
    
