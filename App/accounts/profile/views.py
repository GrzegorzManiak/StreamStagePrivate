import secrets
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
        return JsonResponse({
            'status': 'error',
            'message': '2FA not implemented',
        }, status=status.HTTP_400_BAD_REQUEST)
            
    

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
