from accounts.oauth.oauth import get_oauth_data, link_oauth_account
from django.contrib.auth.hashers import make_password
from django.http.response import JsonResponse
from rest_framework import status

from .email.email import send_email
from .models import Member

"""
    This file contains all things related to the
    creation of a new account.
"""



"""
    Create a new account
    with an oauth id
"""
def create_account_oauth(
    oauth_key: str,
    email: str,
    username: str,
    password: str,
):
    # -- Get the oauth data
    oauth_data = get_oauth_data(oauth_key)

    if oauth_data == False:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid oauth key',
        }, status=status.HTTP_400_BAD_REQUEST)

    # -- Check if the user already has an account
    member = Member.objects.filter(email=email).first()
    if member is not None:
        return JsonResponse({
            'status': 'error',
            'message': 'An account with that email already exists',
        }, status=status.HTTP_400_BAD_REQUEST)


    member = Member.objects.filter(username=username).first()
    if member is not None:
        return JsonResponse({
            'status': 'error',
            'message': 'An account with that username already exists',
        }, status=status.HTTP_400_BAD_REQUEST)

    email = email.lower()
    username = username.lower()
    
    # -- Check if the user's choosen oauth method has a 
    #    verified email
    if oauth_data['data']['email_verified'] is False:
        # -- The user's email is not verified
        #    so we'll need to send a verification email
        return send_email(email, password, username)

    else:
        # -- The user's email is verified
        #    so we can create the account
        member = Member.objects.create(
            username=username,
            email=oauth_data['data']['email'],
            password=make_password(password),
        )

        # -- Remove the oauth id from the session
        link = link_oauth_account(member, oauth_key)

        if link == False:
            # -- Remove the account
            member.delete()

            return JsonResponse({
                'status': 'error',
                'message': 'An error occured while linking the account',
            }, status=status.HTTP_400_BAD_REQUEST)
        

        # -- Return the account
        return member



"""
    Create a new account
    with an email and password
"""
def create_account_email(
    email: str,
    username: str,
    password: str,
):
    # -- Check if the user already has an account
    member = Member.objects.filter(email=email).first()
    if member is not None:
        return JsonResponse({
            'status': 'error',
            'message': 'An account with that email already exists',
        }, status=status.HTTP_400_BAD_REQUEST)


    member = Member.objects.filter(username=username).first()
    if member is not None:
        return JsonResponse({
            'status': 'error',
            'message': 'An account with that username already exists',
        }, status=status.HTTP_400_BAD_REQUEST)

    email = email.lower()
    username = username.lower()
   
    # -- Verify the email
    return send_email(email, password, username)