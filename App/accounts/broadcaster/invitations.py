from accounts.models import BroadcasterContributeInvite, Broadcaster

def get_invitations(user):
    return BroadcasterContributeInvite.objects.filter(invitee=user)

def send_invite(inviter, invitee, broadcaster, message = ""):
    
    invite = BroadcasterContributeInvite(
        inviter = inviter,
        invitee= invitee,
        broadcaster = broadcaster,
        message = message
    )

    invite.save()

def accept_invite(invite:BroadcasterContributeInvite):
    if not invite.is_pending:
        return
    
    invite.is_pending = False
    invite.broadcaster.contributors.add(invite.invitee)

    invite.broadcaster.save()
    invite.save()

def reject_invite(invite:BroadcasterContributeInvite):
    if not invite.is_pending:
        return
    
    invite.is_pending = False

    invite.save()