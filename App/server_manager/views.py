from django.http.response import JsonResponse
from django.shortcuts import render, reverse
from rest_framework import status
from rest_framework.decorators import api_view
from accounts.com_lib import is_admin, success_response
from server_manager.library.router import get_latest_tree
from StreamStage.secrets import NODE_ANNOUNCE_KEY
from server_manager.models import Server
import uuid
import json

from server_manager.library.server import add_server, get_all_servers

@api_view(['POST'])
def announce(request):
    """
        This view is called by a node to announce itself to the 
        network. It will provide us with information about the node
        such as its IP address.

        We will provide the node with a key that it can use
        to authenticate itself to the network.
    """
    
    # -- Check the autherization header for the announce key
    if request.headers.get('Authorization') != NODE_ANNOUNCE_KEY:
        return JsonResponse({
            'error': 'Invalid announce key'
        }, status=status.HTTP_401_UNAUTHORIZED)

    # -- Try parsing the body of the request
    try:
        body = request.data

        # -- Check if the body is valid
        if body is None:
            return JsonResponse({
                'error': 'Invalid body'
            }, status=status.HTTP_400_BAD_REQUEST)

        # -- Check if the body has the required fields
        required = ['rtmp_ip', 'rtmp_port', 'http_ip', 'http_port', 'server_uuid']
        for field in required:
            if body.get(field) is None:
                return JsonResponse({
                    'error': 'Invalid body'
                }, status=status.HTTP_400_BAD_REQUEST)

        # -- Make sure the server UUID is a valid UUID
        try: body['server_uuid'] = uuid.UUID(body['server_uuid'])
        except: return JsonResponse({
                'error': 'Invalid server UUID'
            }, status=status.HTTP_400_BAD_REQUEST)

        # -- Add the server to the database
        server = add_server(
            body['server_uuid'],
            body['rtmp_ip'],
            body['rtmp_port'],
            body['http_ip'],
            body['http_port'],
        )   

        # -- Check if the server was added
        if not server:
            return JsonResponse({
                'error': 'Error adding server'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # -- Return the server
        return JsonResponse(
            server.serialize(),
            status=status.HTTP_200_OK
        )

    except:
        return JsonResponse({
            'error': 'Invalid body'
        }, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST', 'GET'])
def heartbeat(request):
    """
        This view is called by a node to let us know that it is
        still active. We will use this to determine if the node
        is still active and keep track of the node's health.

        The server will provide us with usage statistics about the
        node, such as CPU usage, memory usage, disk usage, etc,
        tx/rx bytes, etc. 

        GET: Used to create/instantiate a heartbeat.
        POST: Used to update a heartbeat.
    """



@api_view(['POST'])
def authenticate(request):
    """
        This view is called by a node to authenticate different
        connections to the node, eg broadcasters, other relay
        nodes trying to ingest content from that node, etc.

        The token will be placed in the body of the request
        in the format:
            VIEWER <token>
            BROADCASTER <token>
            ROOT_RELAY <token>
            RELAY <token>
            
        Tokens can be sent to us in an array as to save on
        resources, eg:
            [
                {
                    'token': <token>,
                    'type': <type>
                },
                {
                    'token': <token>,
                    'type': <type>
                }
            ]

        The response will be a JSON object with the following
        format:
            [
                {
                    'token': <token>,
                    'status': <status>
                },
                {
                    'token': <token>,
                    'status': <status>
                }
            ]
    """



@api_view(['POST'])
def streams(request):
    """
        When a node wants to start to ingest content from a broadcaster
        it first authenticates the broadcaster, than it calls this view to
        announce the incoming stream.

        From here we can than route the stream to the appropriate node(s).
    """
    


###
### Data visualization views
###
@api_view(['GET'])
@is_admin()
def visualize_srr_tree(request):
    """
        This view is used to visualize the SRR tree.
    """
    
    return render(
        request, 
        'visualize_srr_tree.html',
        context={
            'get_srr_tree': reverse('get_srr_tree')
        }
    )



@api_view(['GET'])
@is_admin()
def get_srr_tree(request):
    """
        This view is used to get the SRR tree.
    """
    
    return success_response(
        "Successfully retrieved SRR tree.",
        {
            'tree': json.loads(get_latest_tree()),
            'servers': get_all_servers(False)
        }
    )