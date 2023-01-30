from django.db import models
from django.core.validators import (
    MinLengthValidator, 
    validate_ipv4_address
)
from server_manager.library import ServerMode

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
            ('I', 'Ingest'),
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
        # TODO: Add a check if the server is being set to a different mode
        # whilst other models are referencing it as an ingest server
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
        try: validate_ipv4_address(ip)
        except ValueError: raise ValueError('Invalid IP')

        # Validate the port
        if port < 0 or port > 65535:
            raise ValueError('Invalid port')

        # TODO: Here we would spawn a thread to
        # monitor the heartbeat of the server
        # but we haven't implemented the 
        # heartbeat system yet

        self.ip = ip
        self.port = port
