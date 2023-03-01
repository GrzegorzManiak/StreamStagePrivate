from django.db import models
from accounts.models import Member, Broadcaster
from events.models import Event
from StreamStage.identifiers import new_application_id

# Create your models here.

STATUS_WAITING = "W"
STATUS_APPROVED = "A"
STATUS_REJECTED = "R"

status_friendly_list = [
    (STATUS_WAITING, "Waiting"),
    (STATUS_APPROVED, "Approved"),
    (STATUS_REJECTED, "Rejected")
]

# Application to become a Streamer
class StreamerApplication(models.Model):
    application_id = models.CharField(primary_key=True, max_length=9, default=new_application_id)
    applicant = models.ForeignKey(Member, on_delete=models.CASCADE, null=False)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, null=True)
    submitted = models.DateTimeField("Submitted On", auto_now=True)
    status = models.TextField(choices=status_friendly_list, default=STATUS_WAITING)

    submission_statement = models.TextField("Submission Statement", max_length=1000)

    processed_by = models.ForeignKey(Member, related_name="streamer_processed_by", on_delete=models.DO_NOTHING, null=True)

    def approve(self):
        self.applicant.is_streamer = True
        self.applicant.save()
        self.status = STATUS_APPROVED
        self.save()

    def reject(self):
        self.event.delete()
        self.status = STATUS_REJECTED

# Application to stream an event
class EventApplication(models.Model):
    application_id = models.CharField(primary_key=True,max_length=9,default=new_application_id)
    applicant = models.ForeignKey(Member, null=False, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    submitted = models.DateTimeField("Submitted On", auto_now=True)
    status = models.TextField(choices=status_friendly_list, default=STATUS_WAITING)

    processed_by = models.ForeignKey(Member, related_name="event_processed_by", null=True, on_delete=models.DO_NOTHING)

# Application to become a Broadcaster
class BroadcasterApplication(models.Model):
    application_id = models.CharField(primary_key=True,max_length=9,default=new_application_id)
    applicant = models.ForeignKey(Member, null=False, on_delete=models.CASCADE)
    broadcaster = models.ForeignKey(Broadcaster, null=False, on_delete=models.CASCADE)
    submitted = models.DateTimeField("Submitted On", auto_now=True)
    status = models.TextField(choices=status_friendly_list, default=STATUS_WAITING)

    submission_statement = models.TextField("Submission Statement", max_length=1000)

    processed_by = models.ForeignKey(Member, related_name="broadcaster_processed_by", null=True, on_delete=models.DO_NOTHING)