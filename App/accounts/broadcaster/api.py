from accounts.com_lib import invalid_response, error_response, required_data, success_response
from rest_framework.decorators import api_view
from accounts.models import Member, Broadcaster
from .api_auth import can_edit_broadcaster

@api_view(['POST'])
@required_data(['id', 'name', 'biography'])
@can_edit_broadcaster
def edit_broadcaster_details(request, broadcaster:Broadcaster, data):

    broadcaster.name = data['name']
    broadcaster.biography = data['biography']

    if "pfp" in data:
        pass

    if "banner" in data:
        pass

    return success_response('Successfully updated broadcaster details.')
