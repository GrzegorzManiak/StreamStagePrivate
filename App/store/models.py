from django.db import models
from accounts.models import Member
from events.models import Event, EventShowing, Category

from StreamStage.identifiers import new_ticket_id

class Ticket(models.Model):
    ticket_id = models.CharField(primary_key=True, unique=True, max_length=20, default=new_ticket_id)
    event = models.ForeignKey(Event, null=True, on_delete=models.DO_NOTHING) # if event is deleted - keep ticket

    purchased_date = models.DateTimeField(auto_now_add=True)

    showing = models.ForeignKey(EventShowing, null=True, on_delete=models.DO_NOTHING) # nullable - can buy ticket without specific showing?

    ticket_price = models.FloatField("Price")
    ticket_type = models.CharField("Ticket Type", max_length=20) # 'Online' / 'Special' - yadda yadda

class FlexibleTicket(Ticket):
    valid_date_start = models.DateTimeField()
    valid_date_end = models.DateTimeField()

class AccessPass(models.Model):
    pass_id = models.CharField(primary_key=True, unique=True, max_length=20, default=new_ticket_id)
    
    purchased_date = models.DateTimeField(auto_now_add=True)
    valid_until_date = models.DateTimeField(null=False)

    pass_price = models.FloatField("Price")