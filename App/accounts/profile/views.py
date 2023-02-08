import secrets
import time

from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.decorators import api_view

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
            'send_verification': "profile" + reverse_lazy('send_verification'),
            'resend_verification': "email" + reverse_lazy('resend_key'),
            'remove_verification': "email" + reverse_lazy('remove_key'),
            'recent_verification': "email" + reverse_lazy('recent_key'),
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

    # -- Check if the mode is 2FA or Email
    mode = request.data.get('mode', None)
    if mode is None:
        return JsonResponse({
            'status': 'error',
            'message': 'Missing mode',
        }, status=status.HTTP_400_BAD_REQUEST)

    # -- Check if the user is logged in
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'You are not logged in',
        }, status=status.HTTP_401_UNAUTHORIZED)

    
    match mode:
        case'email':
            key = secrets.token_urlsafe(32)
            new_key = add_key(request.user, validate(key))

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


        case '2fa': return JsonResponse({
            'status': 'error',
            'message': '2FA not implemented',
        }, status=status.HTTP_400_BAD_REQUEST)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid mode',
    }, status=status.HTTP_400_BAD_REQUEST)

            
    
