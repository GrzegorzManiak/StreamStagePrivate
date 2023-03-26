from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from accounts.com_lib import invalid_response, required_data, not_authenticated, success_response
from accounts.models import Member, SecurityPreferences
from StreamStage.models import Statistics

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
@not_authenticated()
@required_data(['email', 'password', 'username'])
def send_reg_verification(request, data):


    # -- Check if have an authorization header
    oauth_token = None
    if 'Authorization' in request.headers:
        oauth_token = request.headers['Authorization']

        # -- Validate the token
        if get_oauth_data(oauth_token) is None:
            return invalid_response('Authorization header is invalid')


    # -- Check if the username is taken
    if username_taken(data['username']): return invalid_response('Username is taken')
    if email_taken(data['email']): return invalid_response('Email is taken')


    # -- Check if an oauth token was provided
    #    and if its email is verifiedq
    if oauth_token is not None:

        # -- Get the oauth data
        oauth_data = get_oauth_data(oauth_token)
        user = Member.objects.filter(email=oauth_data['data']['email'].lower()).first()
        email_verified = oauth_data['data']['email_verified']
        if user != None: email_verified = False



        # -- Check if the email is verified
        if email_verified is False:
            keys = start_email_verification(
                data['email'].lower(), 
                data['password'], 
                data['username'], 
                oauth_token
            )

            return success_response('Email sent', {
                'type': 'not_verified',
                'resend_token': keys[1],
                'verify_token': keys[2],
            })



        elif email_verified is True:
            # -- Get the email from the oauth data
            email = oauth_data['data']['email'].lower()

            # -- The user's email is verified
            #    so we can create the account
            new_member = Member.objects.create(
                username=data['username'].lower(),
                cased_username=data['username'],
                email=email.lower(),
                password=make_password(data['password']),
            )

            # -- Link the oauth account
            link_oauth_account(new_member, oauth_token)
            Statistics.log('accounts', 'register')
            new_member.add_pic_from_url(oauth_data['data']['picture'], 'pfp')
            

            # -- If the account was not created successfully
            if isinstance(new_member, JsonResponse):
                return new_member

            # -- Return the token
            return success_response('Account created successfully', {
                'type': 'verified',
                'token': generate_key(new_member)
            }, status.HTTP_201_CREATED)


        return invalid_response('Email is not verified')
    


    # -- If we dont have an oauth token
    else: 
        keys = start_email_verification(
            data['email'].lower(), 
            data['password'], 
            data['username']
        )

        return success_response('Email sent', {
            'type': 'not_verified',
            'resend_token': keys[1],
            'verify_token': keys[2],
        })
