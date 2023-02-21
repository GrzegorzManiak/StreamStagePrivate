from django.db import models
from accounts.models import Member, Broadcaster
from events.models import Event
from .util import new_application_id

# Create your models here.

STATUS_LIST = [ ("W", "WAITING"), ("A", "APPROVED"), ("R", "REJECTED")]

class StreamerApplication(models.Model):
    application_id = models.CharField(primary_key=True,max_length=9,default=new_application_id)
    applicant = models.ForeignKey(Member, null=False, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    submitted = models.DateTimeField("Submitted On")
    status = models.TextField(choices=STATUS_LIST, default="WAITING")

    submission_statement = models.TextField("Submission Statement", max_length=1000)

    def approve(self):
        self.applicant.is_streamer = True
        self.status = "APPROVED"

    def reject(self):
        self.event.delete()
        self.status = "REJECTED"

class EventApplication(models.Model):
    application_id = models.CharField(primary_key=True,max_length=9,default=new_application_id)
    applicant = models.ForeignKey(Member, null=False, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    submitted = models.DateTimeField("Submitted On")
    status = models.TextField(choices=STATUS_LIST, default="WAITING")

class BroadcasterApplication(models.Model):
    application_id = models.CharField(primary_key=True,max_length=9,default=new_application_id)
    applicant = models.ForeignKey(Member, null=False, on_delete=models.CASCADE)
    broadcaster = models.ForeignKey(Broadcaster, null=False, on_delete=models.CASCADE)
    submitted = models.DateTimeField("Submitted On")
    status = models.TextField(choices=STATUS_LIST, default="WAITING")

    submission_statement = models.TextField("Submission Statement", max_length=1000)