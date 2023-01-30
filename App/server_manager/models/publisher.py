from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
import uuid

class Publisher(models.Model):

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
    )

    name = models.CharField(
        validators=[
            MinLengthValidator(3)
        ],
        max_length=64,
    )

    description = models.TextField()

    # ========= Black/white server list ========= #

    # TODO: Implement this field properly once
    #       the server model is implemented

    list_type = models.CharField(
        max_length=1,
        choices=[
            ('B', 'Blacklist'),
            ('W', 'Whitelist'),
        ],
        default='B',
    )

    # list = models.ManyToManyField(
    #     Server,
    #     through='ServerList',
    #     through_fields=('publisher', 'server'),
    # )

    # =========================================== #

