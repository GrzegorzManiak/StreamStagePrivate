import secrets
import pyotp
import time

from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.decorators import api_view

from django_countries.fields import CountryField
from timezone_field import TimeZoneField

from accounts.oauth.oauth import get_all_oauth_for_member, format_providers
from accounts.email.verification import add_key, send_email
from accounts.models import Member, LoginHistory, oAuth2

from .profile import update_profile

@api_view(['GET'])
def profile(request):

    # -- Make sure that the user is logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # -- Construct the context
    context = {
        'user': request.user,
        'has_tfa': request.user.tfa_secret is not None,
        'countries': CountryField().countries,
        'timezones': TimeZoneField().get_choices(),
        'api': {
            'send_verification': reverse_lazy('send_verification'),
            'resend_verification': reverse_lazy('resend_key'),
            'remove_verification': reverse_lazy('remove_key'),
            'recent_verification': reverse_lazy('recent_key'),
            'security_info': reverse_lazy('security_info'),
            'update_profile': reverse_lazy('update_profile'),
            'remove_oauth': reverse_lazy('remove_oauth'),
            'extend_session': reverse_lazy('extend_session'),
            'setup_mfa': reverse_lazy('setup_mfa'),
            'verify_mfa': reverse_lazy('verify_mfa'),
            'disable_mfa': reverse_lazy('disable_mfa'),
        },

        'oauth': format_providers()
    }

    # -- Render the profile page
    return render(
        request, 
        'profile.html', 
        context=context
    )



"""
    This view is responsible for verifying the user
    before they can access the security page
"""
validated_requests = []

def validate(
    key: str,
):
    def rf(user: Member):
        validated_requests.append({
            'user': user,
            'key': key,
            'time': time.time(),
        })

    return rf

def is_valid(
    key: str, 
    valid_for: int = 60 * 60 * 15 # 15 Minutes
) -> bool:
    for req in validated_requests:
        if req['key'] == key:
            
            # -- Check if the key is expired
            if time.time() - int(req['time']) > valid_for:
                validated_requests.remove(req)
                return False
            
            else: return True


    return False


@api_view(['POST'])
def send_verification(request):

    # -- Check if the user is logged in
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'You are not logged in',
        }, status=status.HTTP_401_UNAUTHORIZED)

    
    if request.user.tfa_secret is None:
        key = secrets.token_urlsafe(32)
        new_key = add_key(
            request.user, 
            request.user.email, 
            validate(key)
        )

        res = send_email(new_key[0])

        if res[0] is False:
            return JsonResponse({
                'status': 'error',
                'message': res[1],
            }, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({
            'status': 'success',
            'message': 'Email sent',
            'access_key': key,
            'resend_key': new_key[1],
            'verify_key': new_key[2],
        }, status=status.HTTP_200_OK)


    else: 
        # -- Get the mfa code
        mfa_code = request.data.get('mfa', None)

        # -- Check if the mfa code is valid
        if mfa_code is None:
            return JsonResponse({
                'status': 'error',
                'message': 'No MFA code provided',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # -- Check if the mfa code is valid
        totp = pyotp.TOTP(request.user.tfa_secret)
        if not totp.verify(mfa_code):
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid MFA code',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # -- Add the key
        key = secrets.token_urlsafe(32)
        validated_requests.append({
            'user': request.user,
            'key': key,
            'time': time.time(),
        })

        # -- Send it back to the user
        return JsonResponse({
            'status': 'success',
            'message': 'MFA code is valid',
            'access_key': key,
            'resend_key': '',
            'verify_key': '',
        }, status=status.HTTP_200_OK)

    

@api_view(['POST'])
def security_info(request):
    # -- Make sure that the user is logged in
    if not request.user.is_authenticated: return JsonResponse({
            'status': 'error',
            'message': 'You are not logged in',
        }, status=status.HTTP_401_UNAUTHORIZED)


    # -- Check if they provided a token
    token = request.data.get('token', None)
    if token is None: return JsonResponse({
            'status': 'error',
            'message': 'No token provided',
        }, status=status.HTTP_400_BAD_REQUEST)
    

    # -- Check if the token is valid
    if not is_valid(token): return JsonResponse({
        'status': 'error',
        'message': 'Invalid token',
    }, status=status.HTTP_400_BAD_REQUEST)
    token_data = None
    for req in validated_requests:
        if req['key'] == token:
            token_data = req
            break

    # -- Return security data
    user = request.user
    return JsonResponse({
        'status': 'success',
        'message': 'Token is valid',
        'data': {
            'email': user.email,
            'dob': user.date_of_birth,
            'tfa': user.tfa_secret is not None,
            'access_level': user.access_level,
            'max_keys': user.max_keys,
            'is_streamer': user.is_streamer,
            'is_broadcaster': user.is_broadcaster,
            'is_admin': user.is_staff,
            'over_18': user.is_over_18(),
            'service_providers': get_all_oauth_for_member(user),
            'login_history': [
                entry.serialize() for entry in LoginHistory.objects.filter(member=user).order_by('-time')[:10]
            ],
            'meta': {
                'started': token_data['time'],
                'expires': token_data['time'] + 60 * 60 * 15,
            }
        }
    }, status=status.HTTP_200_OK)



@api_view(['POST'])
def update_profile(request):

    # -- Make sure that the user is logged in
    if not request.user.is_authenticated: return JsonResponse({
        'status': 'error',
        'message': 'You are not logged in',
    }, status=status.HTTP_401_UNAUTHORIZED)


    # -- Get the data
    data = request.data


    # -- Check if they provided a token
    token = request.data.get('token', None)
    if token is not None:
        # -- Check if the token is valid
        valid = False
        for req in validated_requests:
            if req['key'] == token:
                validated_requests.remove(req)
                valid = True

        if valid == False: return JsonResponse({
            'status': 'error',
            'message': 'Invalid token',
        }, status=status.HTTP_400_BAD_REQUEST)

        # -- Update the profile
        return update_profile(data, True)
    
    else:
        # -- Update the profile
        return update_profile(data, False)
    


@api_view(['POST'])
def remove_oauth(request):
    # -- Make sure the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': 'Not authenticated'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # -- Get the token
    token = request.data.get('token', None)
    if token is None:
        return JsonResponse({
            'message': 'No token provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # -- Check if the token is valid
    if not is_valid(token): return JsonResponse({
        'status': 'error',
        'message': 'Invalid token',
    }, status=status.HTTP_400_BAD_REQUEST)

    # -- Get the oauth id
    oauth_id = request.data.get('oauth_id', None)
    if oauth_id is None:
        return JsonResponse({
            'message': 'No oauth id provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # -- Get the oauth
    oauth = oAuth2.objects.filter(
        id=oauth_id,
        user=request.user
    ).first()

    if oauth is None:
        return JsonResponse({
            'message': 'Invalid oauth'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # -- Delete the oauth
    oauth.delete()

    return JsonResponse({
        'message': 'Success'
    }, status=status.HTTP_200_OK)



@api_view(['POST'])
def extend_session(request):
    # -- Make sure the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': 'Not authenticated'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # -- Get the token
    token = request.data.get('token', None)
    if token is None:
        return JsonResponse({
            'message': 'No token provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # -- Check if the token is valid
    if not is_valid(token): return JsonResponse({
        'status': 'error',
        'message': 'Invalid token',
    }, status=status.HTTP_400_BAD_REQUEST)
    token_data = None
    for req in validated_requests:
        if req['key'] == token:
            token_data = req
            break

    # -- Extend the session
    token_data['time'] = time.time()

    return JsonResponse({
        'message': 'Success'
    }, status=status.HTTP_200_OK)




"""
    2FA

    Once a user request to setup MFA, a token will be generated
    and added to the below list with a reference to the user,
    the token will be valid for 15 minutes, after which it will
    be removed from the list.

    The user will then take the token and use it to setup MFA
    and they will be prompted to enter the token, if the token
    is valid, MFA will be setup for the user.

    If not, the user will be prompted to try again.


    {
        'user': <user>,
        'token': <token>,
        'time': <time>
    }
"""
temp_mfa_tokens = []

@api_view(['POST'])
def setup_mfa(request):
    # -- Make sure the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': 'Not authenticated'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # -- Get the token
    token = request.data.get('token', None)
    if token is None:
        return JsonResponse({
            'message': 'No token provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # -- Check if the token is valid
    if not is_valid(token): return JsonResponse({
        'status': 'error',
        'message': 'Invalid token',
    }, status=status.HTTP_400_BAD_REQUEST)
   
    # -- Check if the user has MFA enabled
    if request.user.tfa_secret is not None:
        return JsonResponse({
            'message': 'MFA is already enabled'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # -- Check if a user already has a token
    #    if so, remove it
    for temp_token in temp_mfa_tokens:
        if str(temp_token['user']['id']) == str(request.user.id):
            temp_mfa_tokens.remove(temp_token)
            break

    # -- Generate a token
    mfa_token = pyotp.random_base32()
    temp_mfa_tokens.append({
        'user': request.user,
        'token': mfa_token,
        'time': time.time()
    })

    # -- Send the token to the user
    return JsonResponse({
        'message': 'Success',
        'data': {
            'token': mfa_token
        }
    }, status=status.HTTP_200_OK)



@api_view(['POST'])
def verify_mfa(request):
    # -- Make sure the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': 'Not authenticated'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # -- Get the token
    token = request.data.get('token', None)
    if token is None:
        return JsonResponse({
            'message': 'No token provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # -- Check if the token is valid
    if not is_valid(token): return JsonResponse({
        'status': 'error',
        'message': 'Invalid token',
    }, status=status.HTTP_400_BAD_REQUEST)

    # -- Get the mfa token
    otp = request.data.get('otp', None)
    if otp is None:
        return JsonResponse({
            'message': 'No mfa token provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # -- Check if the user has MFA enabled
    if request.user.tfa_secret is not None:
        return JsonResponse({
            'message': 'MFA is already enabled'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # -- Check if the user has a token
    temp_token = None
    for temp in temp_mfa_tokens:
        if str(temp['user'].id) == str(request.user.id):
            temp_token = temp
            break

    if temp_token is None:
        return JsonResponse({
            'message': 'No token found'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # -- Check if the token is expired
    if time.time() - temp_token['time'] > 60 * 60 * 15: # 15 minutes
        return JsonResponse({
            'message': 'Token expired'
        }, status=status.HTTP_400_BAD_REQUEST)
    

    # -- Check if the otp is valid
    if not pyotp.TOTP(temp_token['token']).verify(otp):
        return JsonResponse({
            'message': 'Invalid token'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # -- Remove the token
    temp_mfa_tokens.remove(temp_token)

    # -- Enable MFA
    request.user.tfa_secret = temp_token['token']
    request.user.save()

    return JsonResponse({
        'message': 'Success'
    }, status=status.HTTP_200_OK)

    

@api_view(['POST'])
def disable_mfa(request):
    # -- Make sure the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': 'Not authenticated'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # -- Get the token
    token = request.data.get('token', None)
    if token is None:
        return JsonResponse({
            'message': 'No token provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # -- Check if the token is valid
    if not is_valid(token): return JsonResponse({
        'status': 'error',
        'message': 'Invalid token',
    }, status=status.HTTP_400_BAD_REQUEST)

    # -- Remove MFA
    request.user.tfa_secret = None
    request.user.save()

    return JsonResponse({
        'message': 'Success'
    }, status=status.HTTP_200_OK)
