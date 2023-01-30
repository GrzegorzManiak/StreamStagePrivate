from django.db import models
from django.core.validators import MinLengthValidator
import uuid
import secrets

class Server(models.Model):

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )

    slug = models.SlugField(
        validators=[
            MinLengthValidator(3)
        ],
        max_length=10,
        unique=True,
    )

    name = models.CharField(
        validators=[
            MinLengthValidator(3)
        ],
        max_length=64,
    )

    mode = models.CharField(
        max_length=2,
        choices=[
            ('I', 'Ingester'),
            ('R', 'Relay'),
            ('RR', 'Root Relay'),
        ],
        default='I',
    )

    secret = models.CharField(
        validators=[
            MinLengthValidator(3),
        ],
        max_length=64,
        default=secrets.token_urlsafe,
    )

    ip = models.GenericIPAddressField(
        protocol='IPv4',
        null=True,
        blank=True,
    )

    port = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    live = models.BooleanField(
        default=False,
    )
