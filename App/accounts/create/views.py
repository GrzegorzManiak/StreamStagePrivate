from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from accounts.models import Member

from .create import start_email_verification, username_taken, email_taken
from accounts.oauth.oauth import get_oauth_data, link_oauth_account
from accounts.auth_lib import generate_key

"""
    :name: Send Verification Email
    :description: This view is used to send a verification email
                  To a user upon registration
    :view: send_reg_verification
"""
@api_view(['POST'])
def send_reg_verification(request):
    # -- Make sure that the user isint already logged in
    if request.user.is_authenticated:
        return JsonResponse({
            'message': 'You are already logged in'
        }, status=status.HTTP_400_BAD_REQUEST)


    # -- Check if have an authorization header
    oauth_token = None
    if 'Authorization' in request.headers:
        oauth_token = request.headers['Authorization']

        # -- Validate the token
        if get_oauth_data(oauth_token) is None:
            return JsonResponse({
                'message': 'Invalid Authorization header, might be expired',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)


    # -- Check the json data
    if (
        'email' not in request.data or 
        'password' not in request.data or 
        'username' not in request.data
    ):
        return JsonResponse({
            'message': 'Missing email or password or username',
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)


    # -- Get the email and password
    email = request.data['email'].lower()
    password = request.data['password']
    username = request.data['username']


    # -- Check if the username is taken
    if username_taken(username):
        return JsonResponse({
            'message': 'Username is taken',
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)

    if email_taken(email):
        return JsonResponse({
            'message': 'Email is taken',
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)


    # -- Check if an oauth token was provided
    #    and if its email is verifiedq
    if oauth_token is not None:

        # -- Get the oauth data
        oauth_data = get_oauth_data(oauth_token)

        # -- Check if the email is verified
        if oauth_data['data']['email_verified'] is False:
            keys = start_email_verification(
                oauth_data['data']['email'].lower(),
                password,
                username,
                oauth_token
            )

            return JsonResponse({
                'status': 'success',
                'token': keys[1],
                'verify_token': keys[2],
                'message': 'Email sent'
            }, status=status.HTTP_200_OK)

        else:
            # -- Get the email from the oauth data
            email = oauth_data['data']['email'].lower()


            # -- The user's email is verified
            #    so we can create the account
            new_member = Member.objects.create(
                username=username,
                cased_username=username.lower(),
                email=email.lower(),
                password=make_password(password),
            )


            link_oauth_account(new_member, oauth_token)


            # -- If the account was not created successfully
            if isinstance(new_member, JsonResponse):
                return new_member

            # -- Generate the token for the user
            token = generate_key(new_member)

            return JsonResponse({
                'message': 'Account created successfully',
                'token': token,
                'status': 'success'
            }, status=status.HTTP_201_CREATED)
    

    # -- If we dont have an oauth token
    else: 
        keys = start_email_verification(email, password, username)
        return JsonResponse({
            'status': 'success',
            'token': keys[1],
            'verify_token': keys[2],
            'message': 'Email sent'
        }, status=status.HTTP_200_OK)
