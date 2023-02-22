from server_manager.models import Server
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def index(request):
    """
        Mostly static page that displays pinned blogs
        and a twitch style of configurations for
        obs
    """
    return render(request, 'index.html', {})


@api_view(['GET'])
def ingests(request):
    """
        Returns a list of servers back to the user
    """
    servers = Server.objects.all()

    # -- Serialize the servers
    serialized = [server.display() for server in servers]

    return render(request, 'ingests.html', {
        'servers': serialized
    })