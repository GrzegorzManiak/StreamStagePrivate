import secrets
import time

from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.decorators import api_view

from accounts.oauth.oauth import get_all_oauth_for_member
from accounts.email.verification import add_key, send_email
from accounts.models import Member

from .forms import compile_objects


@api_view(['GET'])
def profile(request):

    # -- Make sure that the user is logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # -- Construct the context
    context = {
        'user': request.user,
        'api': {
            'send_verification': reverse_lazy('send_verification'),
            'resend_verification': reverse_lazy('resend_key'),
            'remove_verification': reverse_lazy('remove_key'),
            'recent_verification': reverse_lazy('recent_key'),
            'security_info': reverse_lazy('security_info'),
        },

        'pages': compile_objects(request.user),
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
    valid = False
    for req in validated_requests:
        if req['key'] == token:
            validated_requests.remove(req)
            valid = True

    if not valid: return JsonResponse({
        'status': 'error',
        'message': 'Invalid token',
    }, status=status.HTTP_400_BAD_REQUEST)


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
        }
    }, status=status.HTTP_200_OK)