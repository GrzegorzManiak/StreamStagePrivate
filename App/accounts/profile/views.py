from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ..models import Member
from django.shortcuts import render, redirect
from django.urls import reverse
import time
import secrets

from .profile import (
    change_username,
    change_description,
)

from accounts.email.verification import (
    add_key,
    send_email
)

@api_view(['POST'])
def change_details(request):
    # -- Make sure the user is logged in
    if request.user.is_authenticated is False:
        return JsonResponse({
            'status': 'error',
            'message': 'You are not logged in',
        }, status=status.HTTP_401_UNAUTHORIZED)


    # -- Get the user
    user = Member.objects.filter(id=request.user.id).first()
    if user is None:
        return JsonResponse({
            'status': 'error',
            'message': 'You are not logged in',
        }, status=status.HTTP_401_UNAUTHORIZED)

    # -- Get the data
    data = request.data
    if 'description' not in data:
        return JsonResponse({
            'status': 'error',
            'message': 'Missing description',
        }, status=status.HTTP_400_BAD_REQUEST)


    if data['description'] is not None:
        res = change_description(user, data['description'])
        if res[0] is False:
            return JsonResponse({
                'status': 'error',
                'message': res[1],
            }, status=status.HTTP_400_BAD_REQUEST)

    if data['username'] is not None:
        res = change_username(user, data['username'])
        if res[0] is False:
            return JsonResponse({
                'status': 'error',
                'message': res[1],
            }, status=status.HTTP_400_BAD_REQUEST)


    return JsonResponse({
        'status': 'success',
        'message': 'Details changed',
    }, status=status.HTTP_200_OK)




@api_view(['GET'])
def profile(request):

    # -- Make sure that the user is logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # -- Construct the context
    context = {
        'user': request.user,
        'api': {
            'change_details': "profile" + reverse('change_details', urlconf='accounts.profile.urls'),

            'send_verification': "profile" + reverse('send_verification', urlconf='accounts.profile.urls'),
            'resend_verification': "email" + reverse('resend_key', urlconf='accounts.email.urls'),
            'remove_verification': "email" + reverse('remove_key', urlconf='accounts.email.urls'),
            'recent_verification': "email" + reverse('recent_key', urlconf='accounts.email.urls'),
        }
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

            
    