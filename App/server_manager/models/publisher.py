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


    # TODO: Implement these functions once
    #       the server model is implemented
    def add_server(self, server):
        pass

    def remove_server(self, server):
        pass

    def is_server(self, server):
        pass

    def get_servers(self):
        pass

    # ============================== #