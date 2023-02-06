from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework import status
from .email import verify, recent, resend, temp_users
from django.shortcuts import render, redirect


"""
    This view is responsible verifying the user's email
    token
"""
@api_view(['GET'])
def verify_view(request):
    verified = True
    message = ''

    # -- Make sure the user is not logged in
    if request.user.is_authenticated:
        verified = False
        message = 'You are already logged in'

    # -- Get the token
    token = request.GET.get('token', None)
    
    # -- Make sure the token is there
    if token is None:
        verified = False
        message = 'The verification token was not provided'


    # -- Check if the token is valid
    if temp_users.get(token) is None:
        verified = False
        message = 'The verification token is invalid'

    # -- Get the user's details
    if verified:
        resonse = verify(token)
        verified = resonse[0]
        message = resonse[1]

    # -- Build the context
    context = {
        'verified': verified,
        'message': message
    }

    # -- Render the page
    return render(
        request, 
        'verify.html', 
        context=context
    )



"""
    This view is responsible for checking if the user has
    recently verified their email
"""
@api_view(['POST'])
def recent_view(request):
    # -- Make sure the user is not logged in
    if request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Already logged in'
        }, status=status.HTTP_400_BAD_REQUEST)

    # -- Get the token
    verify_token = request.data.get('token')

    # -- Make sure the token is there
    if verify_token is None:
        return JsonResponse({
            'status': 'error',
            'message': 'Verify key not provided'
        }, status=status.HTTP_400_BAD_REQUEST)

    # -- Get the user's details
    return recent(verify_token)



"""
    This view is responsible for resending the verification
    email
"""
@api_view(['POST'])
def resend_view(request):
    # -- Make sure the user is not logged in
    if request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Already logged in'
        }, status=status.HTTP_400_BAD_REQUEST)

    # -- Get the email and token
    email = request.data.get('email')
    resend_key = request.data.get('token')

    if resend_key is None:
        return JsonResponse({
            'status': 'error',
            'message': 'Resend key not provided'
        }, status=status.HTTP_400_BAD_REQUEST)


    # -- Email is changed
    if email is not None:
        return resend(resend_key, email)

    # -- Email stayed the same
    else: return resend(resend_key)
