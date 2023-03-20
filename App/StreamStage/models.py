from django.db import models
import uuid

class SentEmail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email_id = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email