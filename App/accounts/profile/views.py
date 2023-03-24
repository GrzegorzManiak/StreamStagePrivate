import secrets
import pyotp

from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.decorators import api_view

from django_countries.fields import CountryField
from timezone_field import TimeZoneField
from StreamStage.mail import send_template_email
from accounts.com_lib import authenticated, error_response, invalid_response, required_data, success_response

from accounts.oauth.oauth import get_all_oauth_for_member, format_providers
from accounts.email.verification import add_key, send_email
from accounts.models import LoginHistory, oAuth2

from .profile import (
    generate_pat, 
    update_profile, 
    validate_pat, 
    extend_pat, 
    get_pat, 
    revoke_pat, 
    change_email,
    PAT_EXPIRY_TIME
)
from StreamStage.secrets import STRIPE_PUB_KEY

@api_view(['GET'])
@authenticated()
def profile(request):
    # -- Construct the context
    context = {
        'user': request.user,
        'has_tfa': request.user.tfa_secret is not None,
        'countries': CountryField().countries,
        'timezones': TimeZoneField().get_choices(),
        'security_preferences': request.user.security_preferences.serialize(),
        'api': {
            'send_verification': reverse_lazy('send_verification'),
            'resend_verification': reverse_lazy('resend_key'),
            'remove_verification': reverse_lazy('remove_key'),
            'recent_verification': reverse_lazy('recent_key'),
            'security_info': reverse_lazy('security_info'),
            'update_profile': reverse_lazy('update_profile'),
            'remove_oauth': reverse_lazy('remove_oauth'),
            'extend_session': reverse_lazy('extend_session'),
            'close_session': reverse_lazy('close_session'),
            'setup_mfa': reverse_lazy('setup_mfa'),
            'change_email': reverse_lazy('change_email'),
            'verify_mfa': reverse_lazy('verify_mfa'),
            'disable_mfa': reverse_lazy('disable_mfa'),
            'add_payment': reverse_lazy('add_payment'),
            'get_payments': reverse_lazy('get_payments'),
            'remove_payment': reverse_lazy('remove_payment'),
            'start_subscription': reverse_lazy('start_subscription'),
            'get_reviews': reverse_lazy('get_reviews'),
            'update_review': reverse_lazy('update_review'),
            'delete_review': reverse_lazy('delete_review'),
            'change_pfp': reverse_lazy('change_pfp'),
        },
        'stripe': request.user.get_stripe_customer(),
        'stripe_key': STRIPE_PUB_KEY,
        'oauth': format_providers()
    }

    # -- Render the profile page
    return render(
        request, 
        'profile.html', 
        context=context
    )



@api_view(['POST'])
@authenticated()
def send_verification(request):
    def callback(data):
        generate_pat(request.user, key)

    if request.user.tfa_secret is None:
        key = secrets.token_urlsafe(32)
        new_key = add_key(
            request.user, 
            request.user.email, 
            callback
        )

        res = send_email(new_key[0])
        if res[0] is False: return invalid_response(res[1])

        return success_response('Email sent', {
            'access_key': key,
            'resend_key': new_key[1],
            'verify_key': new_key[2],
        })


    else: 
        # -- Get the mfa code
        mfa_code = request.data.get('mfa', None)

        # -- Check if the mfa code is valid
        if mfa_code is None: return error_response(
            'Please provide a MFA code')

        # -- Check if the mfa code is valid
        if request.user.verify_mfa(mfa_code) == False: return invalid_response(
            'Sorry, but it looks like you have provided an invalid MFA code. Please try again.')
        
        # -- Send it back to the user
        return success_response('MFA code is valid', {
            'access_key': generate_pat(request.user),
            'resend_key': '',
            'verify_key': '',
        })

    

@api_view(['POST'])
@authenticated()
@required_data(['token'])
def security_info(request, data):

    # -- Check if the token is valid
    pat = validate_pat(data['token'], request.user)
    if pat[0] == False: return invalid_response(pat[1])
    pat_data = get_pat(data['token'])[0]  

    # -- Return security data
    user = request.user
    return success_response('Security data', {
        'email': user.email,
        'dob': user.date_of_birth,
        'tfa': user.tfa_secret is not None,
        'access_level': user.access_level,
        'max_keys': user.max_keys,
        'is_streamer': user.is_streamer,
        'is_admin': user.is_staff,
        'over_18': user.is_over_18(),
        'service_providers': get_all_oauth_for_member(user),
        'login_history': [
            entry.serialize() for entry in LoginHistory.objects.filter(member=user).order_by('-time')[:10]
        ],
        'meta': {
            'started': pat_data['time'],
            'expires': pat_data['time'] + PAT_EXPIRY_TIME,
        },
        'security_preferences': user.security_preferences.serialize(),
    })



@api_view(['POST'])
@authenticated()
def update_profile_view(request):    

    # -- Get the data
    data = request.data
    res = None

    # -- Check if they provided a token
    token = request.data.get('token', None)
    if token is not None:

        # -- Check if the token is valid
        pat = validate_pat(token, request.user)
        if pat[0] == False: return invalid_response(pat[1])
        res = update_profile(request.user, data, True)
    
    # -- Update the profile
    else: res = update_profile(request.user, data, False)


    # -- Check if the update was successful
    if res[0] == False: return invalid_response(res[1])
    return success_response('Profile updated successfully')
    


@api_view(['POST'])
@authenticated()
@required_data(['token', 'oauth_id'])
def remove_oauth(request, data):
    
    # -- Check if the token is valid
    pat = validate_pat(data['token'], request.user)
    if pat[0] == False: return invalid_response(pat[1])
    
    # -- Get the oauth
    oauth = oAuth2.objects.filter(
        id=data['oauth_id'],
        user=request.user
    ).first()

    if oauth is None: return invalid_response(
        'Sorry, but it looks like you have provided an invalid OAuth ID. Please try again.')
    
    # -- Serialize the oauth
    serialized = oauth.serialize()

    # -- Delete the oauth
    oauth.delete()
    if request.user.security_preferences.email_on_oauth_change:
        send_template_email(request.user, 'oauth_account_removed', serialized)

    # -- Return success
    return success_response('OAuth removed successfully')



@api_view(['POST'])
@authenticated()
@required_data(['token'])
def extend_session(request, data):
    
    # -- Check if the token is valid
    pat = extend_pat(data['token'], request.user)
    if pat[0] == False: return invalid_response(pat[1])
    return success_response('Session extended successfully')



@api_view(['POST'])
@authenticated()
@required_data(['token'])
def close_session(request, data):

    # -- Check if the token is valid
    pat = revoke_pat(data['token'], request.user)
    if pat[0] == False: return invalid_response(pat[1])
    return success_response('Session closed successfully')



@api_view(['POST'])
@authenticated()
@required_data(['token', 'email'])
def change_email_view(request, data):
    
    # -- Check if the token is valid
    pat = validate_pat(data['token'], request.user)
    if pat[0] == False: return invalid_response(pat[1])

    res = change_email(request.user, data['email'])
    if res[0] == False: return invalid_response(res[1])

    # -- Return success
    return success_response('Email changed successfully', {
        'resend_key': res[1],
        'verify_key': res[2],
    })



@api_view(['POST'])
@authenticated()    
@required_data(['image'])
def upload_profile_image(request, data):
    """
        Uploads a profile image to the server
        and saves it to the user's profile
    """ 

    res = request.user.add_profile_pic_from_base64(data['image'])

    # -- Return success
    if res == False: return invalid_response(
        'Sorry, but it looks like you have provided an invalid image. Please try again.')

    return success_response('Profile image uploaded successfully', {
        'image': request.user.get_profile_pic(),
    })