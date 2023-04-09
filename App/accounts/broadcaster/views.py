from django.shortcuts import render
from rest_framework.decorators import api_view
from accounts.forms import BroadcasterUpdateForm

from StreamStage.templatetags.tags import cross_app_reverse

from accounts.models import Broadcaster
from accounts.broadcaster.api_auth import can_edit_broadcaster
from accounts.com_lib import authenticated, required_data, success_response, error_response


# temporary
@api_view(['GET'])
@authenticated()
def edit_broadcasters(request):
    # Create a comma-delimited list of broadcasters this user
    # has access to so that the client script can retrieve data
    # about them.

    broadcasters = ""
    
    for broadcaster in request.user.get_authorized_broadcasters():
        broadcasters += str(broadcaster.id) + ","

    # Trim trailing comma
    broadcasters = broadcasters[:-1]

    update_form = BroadcasterUpdateForm()

    return render(request, 'member_broadcaster.html', 
        context = {
            "broadcaster_id_list": broadcasters,
            "api": {
                "get_broadcaster_details": cross_app_reverse('accounts', 'get_broadcaster_details'),
                "update_broadcaster_details": cross_app_reverse('accounts', 'update_broadcaster_details')
            },
            "update_form": update_form
        }
    )


@api_view(['POST'])
@authenticated()
@required_data(['id', 'biography', 'name', 'profile', 'banner'])
@can_edit_broadcaster()
def update_broadcaster_details(request, broadcaster:Broadcaster, data):

    profile = data['profile']
    banner = data['banner']

    if len(profile) > 0:
        if not broadcaster.set_picture_b64("profile_pic", profile):
            return error_response("Error setting profile picture.")
    
    if len(banner) > 0:
        if not broadcaster.set_picture_b64("banner", banner):
            return error_response("Error setting banner picture.")
    
    broadcaster.biography = data["biography"]
    broadcaster.name = data["name"]

    broadcaster.save()

    return success_response("Successfully updated broadcaster details.")

@api_view(['POST'])
@authenticated()
@required_data(['id'])
@can_edit_broadcaster()
def get_broadcaster_details(request, broadcaster:Broadcaster, data):

    encoded_broadcaster = {
        "id": broadcaster.id,
        "handle": broadcaster.handle,
        "name": broadcaster.name,
        "biography": broadcaster.biography,
        "profile": broadcaster.get_picture("profile_pic"),
        "banner": broadcaster.get_picture("banner")
    }

    return success_response("Retrieved broadcaster details", { "details": encoded_broadcaster })
