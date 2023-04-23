
from accounts.com_lib import authenticated, invalid_response, error_response, required_data, success_response
from rest_framework.decorators import api_view

from events.models import EventShowing

from .live_chat import (
    get_new_messages,
    send_message
)


@api_view(['POST'])
@required_data(['showing_id', 'last'])
@authenticated()
def fetch_new_messages(request, data):
    last = int(data['last'])
    showing_id = data['showing_id']

    try:
        showing = EventShowing.objects.get(showing_id=showing_id)
    except:
        return error_response("Invalid Showing.")


    messages = get_new_messages(request.user, showing_id, last)

    return success_response('Success', {
        'messages': messages
    })


@api_view(['POST'])
@required_data(['showing_id', 'message'])
@authenticated()
def send_new_message(request, data):
    last = int(data['last'])
    showing_id = data['showing_id']

    try:
        showing = EventShowing.objects.get(showing_id=showing_id)
    except:
        return error_response("Invalid Showing.")

    send_message(request.user, showing_id, data['message'])

    return success_response('Success')

