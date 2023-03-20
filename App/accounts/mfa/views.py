# - Imports
from StreamStage.mail import send_template_email
from .mfa import generate_token, delete_duplicate, get_token, verify_temp_otp
from rest_framework.decorators import api_view
from accounts.com_lib import authenticated, invalid_response, required_data, success_response
from accounts.profile import validate_pat


@api_view(['POST'])
@authenticated()
@required_data(['token'])
def setup_mfa(request, data):

    # -- Check if the token is valid
    pat = validate_pat(data['token'], request.user)
    if pat[0] == False: return invalid_response(pat[1])
   
    # -- Check if the user has MFA enabled
    if request.user.tfa_secret is not None:
        return invalid_response('MFA is already enabled for this account')
    
    delete_duplicate(request.user)
    mfa_token = generate_token(request.user)

    # -- Send the token to the user
    return success_response('MFA token generated', { 'token': mfa_token })



@api_view(['POST'])
@authenticated()
@required_data(['token', 'otp'])
def verify_mfa(request, data):
    # -- Check if the token is valid
    pat = validate_pat(data['token'], request.user)
    if pat[0] == False: return invalid_response(pat[1])
    
    # -- Check if the user has MFA enabled
    if request.user.tfa_secret is not None:
        return invalid_response('MFA is already enabled for this account')

    # -- Check if the otp is valid
    verify_mfa_data = verify_temp_otp(request.user, data['otp'])
    if verify_mfa_data[0] == False: return invalid_response(verify_mfa_data[1])

    # -- Remove the token and enable MFA
    request.user.tfa_secret = get_token(request.user)[0]
    request.user.save()
    delete_duplicate(request.user)
    
    # -- Set the recovery codes and email the user
    request.user.set_recovery_codes()
    send_template_email(
        request.user, 
        'mfa_enabled', 
        request.user.get_recovery_codes()
    )

    # -- Return a success response
    return success_response('MFA has been enabled successfully')

    

@api_view(['POST'])
@authenticated()
@required_data(['token'])
def disable_mfa(request, data):
    # -- Check if the token is valid
    pat = validate_pat(data['token'], request.user)
    if pat[0] == False: return invalid_response(pat[1])
    
    # -- Remove MFA
    request.user.tfa_secret = None
    request.user.save()

    # -- Email the user
    if request.user.security_preferences.email_on_mfa_change:
        send_template_email(request.user, 'mfa_disabled')

    return success_response('MFA has been disabled successfully')
