from accounts.com_lib import invalid_response, error_response, required_data, success_response
from rest_framework.decorators import api_view
from accounts.models import Member, Broadcaster
from .api_auth import can_edit_broadcaster

@api_view(['POST'])
@required_data(['id', 'name', 'biography'])
@can_edit_broadcaster
def edit_broadcaster_details(request, broadcaster:Broadcaster, data):
    if not broadcaster.approved:
        return error_response("Cannot edit broadcaster details until application is approved.")

    broadcaster.name = data['name']
    broadcaster.biography = data['biography']

    if "pfp" in data:
        pass

    if "banner" in data:
        pass

    return success_response('Successfully updated broadcaster details.')

@api_view(['GET'])
@required_data(['id'])
@can_edit_broadcaster
def get_broadcaster_details(request, broadcaster:Broadcaster, data):
    """
        Returns the broadcaster with the given id.
    """
    
    return success_response('Successfully retrieved broadcaster', {
        'id': broadcaster.id,
        'handle': broadcaster.handle,
        'over_18': broadcaster.over_18,
        'approved': broadcaster.approved,
        'created': broadcaster.created,
        'updated': broadcaster.updated,
        'name': broadcaster.name,
        'biography': broadcaster.biography,
        'streamer': broadcaster.streamer.id,
        'profile_picture': broadcaster.get_picture('profile_pic'),
        'profile_banner': broadcaster.get_picture('banner')
    })