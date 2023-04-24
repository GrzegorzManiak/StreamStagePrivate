from django.shortcuts import render
from rest_framework.decorators import api_view
from accounts.forms import BroadcasterUpdateForm

from StreamStage.templatetags.tags import cross_app_reverse

from accounts.models import Broadcaster, Member, BroadcasterContributeInvite
from accounts.broadcaster.api_auth import can_edit_broadcaster
from accounts.com_lib import authenticated, required_data, success_response, error_response

from .invitations import is_invited, send_invite, accept_invite, get_invitations, reject_invite


# temporary
@api_view(['GET'])
@authenticated()
def broadcaster_panel(request):
    # Create a comma-delimited list of broadcasters this user
    # has access to so that the client script can retrieve data
    # about them.

    broadcasters = ""
    
    for broadcaster in request.user.get_authorized_broadcasters():
        broadcasters += str(broadcaster.id) + ","

    if len(broadcasters) == 0:
        broadcasters = ':none:'
    else:
        # Trim trailing comma
        broadcasters = broadcasters[:-1]

    update_form = BroadcasterUpdateForm()

    return render(request, 'broadcaster.html', 
        context = {
            "broadcaster_id_list": broadcasters,
            "api": {
                "get_broadcaster_details": cross_app_reverse('accounts', 'get_broadcaster_details'),
                "update_broadcaster_details": cross_app_reverse('accounts', 'update_broadcaster_details'),

                "fetch_invites": cross_app_reverse('accounts', 'fetch_contribute_invites'),
                "send_invite": cross_app_reverse('accounts', 'send_contribute_invite'),
                "respond_invite": cross_app_reverse('accounts', 'respond_contribute_invite'), 
                "remove_contributor": cross_app_reverse('accounts', 'remove_contributor')
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

    contributors = []

    for contributor in broadcaster.contributors.all():
        print(contributor.get_profile_pic() )
        contributors.append({
            "username": contributor.username,
            "url": cross_app_reverse('homepage', 'user_profile', {"username": contributor.username}),
            "profile": contributor.get_profile_pic() or '/static/images/default_event_cover.png',
        })

    encoded_broadcaster = {
        "id": broadcaster.id,
        "handle": broadcaster.handle,
        "name": broadcaster.name,
        "biography": broadcaster.biography,
        "profile": broadcaster.get_picture("profile_pic"),
        "banner": broadcaster.get_picture("banner"),
        "url": cross_app_reverse('homepage', 'broadcaster_profile', {"username": broadcaster.handle}),
        "approved": broadcaster.approved,
        "contributors": contributors
    }

    return success_response("Retrieved broadcaster details", { "details": encoded_broadcaster })

@api_view(['POST'])
@authenticated()
def fetch_invites(request):
    encoded_invites = []

    for invite in get_invitations(request.user):
        encoded_invites.append({
            "id":invite.id,
            "inviter": invite.inviter.cased_username,
            "broadcaster": invite.broadcaster.handle,
            "bc_profile": invite.broadcaster.get_picture("profile_pic"),
            "bc_url": cross_app_reverse('homepage', 'broadcaster_profile', {"username": invite.broadcaster.handle}),
            "message": invite.message
        })

    return success_response("Successfully fetched invitations.", { "invites": encoded_invites })

@api_view(['POST'])
@authenticated()
@required_data(['id', 'invitee', 'message'])
@can_edit_broadcaster()
def send_contribute_invite(request, broadcaster:Broadcaster, data):
    try:
        user = Member.objects.get(username=data['invitee'])
    except:
        return error_response("Couldn't find user by that username.")
    
    if broadcaster.streamer == user:
        return error_response("Given user is this broadcaster's founder.")

    if broadcaster.contributors.contains(user):
        return error_response("This user is already a contributor.")
    
    if is_invited(user, broadcaster):
        return error_response("This user is already invited to contribute.")

    
    send_invite(request.user, user, broadcaster, data['message'])

    return success_response("Invitation to contribute has been sent!")

@api_view(['POST'])
@authenticated()
@required_data(['id', 'contributor'])
@can_edit_broadcaster()
def remove_contributor(request, broadcaster:Broadcaster, data):
    try:
        user = Member.objects.get(username=data['contributor'])
    except:
        return error_response("Couldn't find user by that username.")
    
    if broadcaster.streamer == user:
        return error_response("Given user is this broadcaster's founder.")

    if not broadcaster.contributors.contains(user):
        return error_response("This user is not a contributor.")
    
    broadcaster.contributors.remove(user)
    
    return success_response("Removed contributor.")

@api_view(['POST'])
@authenticated()
@required_data(['id', 'response'])
def respond_to_invite(request, data):

    try:
        invite = BroadcasterContributeInvite.objects.get(id=data['id'])
    except:
        return error_response("Couldn't find that invite.")
    
    if not invite.is_pending:
        return error_response("You have already responded to this invite.")
    
    if data['response'] == "y":
        accept_invite(invite)
    else:
        reject_invite(invite)

    return success_response("Invitation to contribute has been sent!")
