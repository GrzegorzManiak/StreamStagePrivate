from django.db import models
from accounts.models import Member
from events.models import Event, EventShowing

class Ticket(models.Model):
    ticket_id = models.CharField(primary_key=True, unique=True, max_length=20)
    event = models.ForeignKey(Event)
    showing = models.ForeignKey(EventShowing, null=True) # nullable - can buy ticket without specific showing?
    ticket_price = models.FloatField("Price")
    ticket_type = models.CharField("Ticket Type", max_length=20) # 'Online' / 'Special' - yadda yadda

