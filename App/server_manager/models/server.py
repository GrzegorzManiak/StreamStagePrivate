from django.db import models
from django.core.validators import (
    MinLengthValidator, 
    ip_address_validators
)
from library import ServerMode

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

    def __str__(self):
        return self.name


    # ========= Functions ========= #
    def set_mode(self, mode: ServerMode) -> None or ValueError:
        mode = mode.to_string()

        if mode is not None: self.mode = mode
        else: raise ValueError('Invalid server mode')

    def get_mode(self) -> ServerMode or ValueError:
        mode = ServerMode.from_string(self.mode)

        if mode is not None: return mode
        else: raise ValueError('Invalid server mode')

    def announce(self, ip, port, hb_id) -> None:
        self.live = True
        
        # Validate the IP and port
        try: ip_address_validators('ipv4', ip)
        except: raise ValueError('Invalid IP address')

        # Validate the port
        if port < 0 or port > 65535:
            raise ValueError('Invalid port')

        # TODO: Here we would spawn a thread to
        # monitor the heartbeat of the server
        # but we haven't implemented the 
        # heartbeat system yet

        self.ip = ip
        self.port = port

        self.save()


    def save(self, *args, **kwargs):
        # Validate that if live is True, then the IP and port are not None
        if self.live:
            if self.ip is None or self.port is None:
                raise ValueError('Server is live, but IP or port is None')

        super().save(*args, **kwargs)

