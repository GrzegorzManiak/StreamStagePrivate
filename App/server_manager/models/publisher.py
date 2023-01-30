from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
import uuid
from .server import Server

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

    list_type = models.CharField(
        max_length=1,
        choices=[
            ('B', 'Blacklist'),
            ('W', 'Whitelist'),
        ],
        default='B',
    )

    server_list = models.ManyToManyField(
        Server,
    )

    # =========================================== #

    def __str__(self):
        return self.name


    # ========= Functions ========= #
    def add_member(self, member):
        # Make sure the member is not already in the list
        if member not in self.members.all():
            self.members.add(member)

    def remove_member(self, member):
        # Make sure the member is in the list
        if member in self.members.all():
            self.members.remove(member)

    def is_member(self, member):
        return member in self.members.all()

    def get_members(self):
        return self.members.all()


    def add_server(self, server: Server) -> bool: 
        # Make sure the server is not already in the list
        if server not in self.server_list.all():
            self.server_list.add(server)
            return True
        
        return False

    def remove_server(self, server: Server):
        # Make sure the server is in the list
        if server in self.server_list.all():
            self.server_list.remove(server)
            return True

        return False

    def has_server(self, server: Server) -> bool:
        return server in self.server_list.all()

    def get_servers(self):
        return self.server_list.all()

    # ============================== #