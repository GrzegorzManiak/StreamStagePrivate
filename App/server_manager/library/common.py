from enum import Enum
from django.http.response import JsonResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework import status
from functools import wraps
from django.apps import apps

from accounts.com_lib import invalid_response

class ServerMode(Enum):
    INGEST = 1
    RELAY = 2
    ROOT_RELAY = 3

    def to_string(self) -> str or None:
        match self:
            case ServerMode.INGEST: return 'I'
            case ServerMode.RELAY: return 'R'
            case ServerMode.ROOT_RELAY: return 'RR'

        return None

    def from_string(mode: str) -> any or None:
        match mode:
            case 'I': return ServerMode.INGEST
            case 'R': return ServerMode.RELAY
            case 'RR': return ServerMode.ROOT_RELAY

        return None
    


"""
    :name: is_node
    :description: This decorator will determine if the node is valid
"""
def is_node():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # -- Try and get a node that matches both parameters
            try: 
                # -- Get the Authorization header and the id
                auth = request.headers.get('Authorization')
                node_id = request.headers.get('Node-ID')

                # -- Check if the auth header is valid
                if auth is None or node_id is None:
                    return invalid_response('Invalid node', 401)
                
                server = apps.get_model('server_manager', 'Server')
                server.objects.get(secret=auth, id=node_id)

            except: return invalid_response('Invalid node', 401)

            # -- Call the original function with the request object
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator