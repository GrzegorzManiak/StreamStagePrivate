from django.db import models
from django.core.validators import MinLengthValidator
import secrets
import uuid

class StreamAccess(models.Model):

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )

    user = models.ForeignKey(
        'Member',
        on_delete=models.CASCADE,
        related_name='stream_access'
    )

    key = models.CharField(
        validators=[
            MinLengthValidator(32)
        ],
        max_length=64,
        default=secrets.token_hex(16)
    )

    # ========= Temporary ========= #
    # TODO: Remove this field after 
    #       the stream is implemented
    # ============================= #
    stream = models.TextField()


    def __str__(self):
        return f'{self.user} - {self.stream}'
