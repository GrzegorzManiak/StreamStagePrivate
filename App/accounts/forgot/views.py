from accounts.com_lib import not_authenticated, error_response, invalid_response, required_data, success_response, impersonate
from accounts.models import Member
from rest_framework.decorators import api_view
import secrets
from accounts.create.create import strong_password

from .forgot import (
    request_password_reset,
    verify_password_reset
)

@api_view(['post'])
@not_authenticated()
@required_data(['eom'])
def init_change_password(request, data):

    # -- Attempt to get the user
    eom = data['eom'].lower()
    user = None

    try: # -- Try to get the user by email
        user = Member.objects.filter(email=eom).first()
    except: user = None
    print(user)
    if not user:
        try: # -- Try to get the user by username
            user = Member.objects.filter(username=eom).first()
        except: user = None
    print(user)

    # -- If the user does not exist
    SUCCESS_RESPONSE = "If the Email / Username you entered is valid, you will receive an email shortly."
    if not user: return success_response(SUCCESS_RESPONSE, {
        'verify_token': secrets.token_urlsafe(32),
        'access_token': secrets.token_urlsafe(32),
        'resend_token': secrets.token_urlsafe(32),
    })

    # -- Request a password reset
    keys = request_password_reset(user)
    if keys[0] == False: return success_response(SUCCESS_RESPONSE, {
        'verify_token': secrets.token_urlsafe(32),
        'access_token': secrets.token_urlsafe(32),
        'resend_token': secrets.token_urlsafe(32),
    })

    # -- Return the success response
    return success_response(SUCCESS_RESPONSE, {
        'verify_token': keys[1],
        'access_token': keys[0],
        'resend_token': keys[2],
    })



@api_view(['post'])
@not_authenticated()
@required_data(['token', 'password'])
def change_password(request, data):
    # -- Check if the password is strong
    if not strong_password(data['password']): 
        return invalid_response('Password is not strong enough')

    # -- Verify the password reset
    verifed = verify_password_reset(data['token'])
    if verifed[0] == False: return invalid_response(verifed[1])

    # -- Get the user
    user = verifed[1]
    
    # -- Change the password
    user.set_password(data['password'])
    user.save()

    # -- Return the success response
    return success_response('Successfully changed password')