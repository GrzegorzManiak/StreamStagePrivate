from django.contrib.auth import login as dj_login, logout as dj_logout
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.decorators import api_view
from accounts.com_lib import (
    authenticated, 
    not_authenticated,
    invalid_response, 
    required_headers,
    success_response,
    required_data
)
from StreamStage.mail import send_template_email
from StreamStage.models import Statistics

from accounts.auth_lib import authenticate_key, generate_key
from accounts.models import Member, LoginHistory, SecurityPreferences
from accounts.oauth.oauth import format_providers
from accounts.email.verification import add_key, send_email
import secrets

@api_view(['GET'])
@not_authenticated()
def login(request):
    """
        This view is used to get a token
        aka, login
    """
    # -- Render the login page
    return render(
        request, 
        'login.html', 
        context={
            'providers': format_providers(),
            'token': reverse('token'),
            'get_token': reverse('get_token'),
            'register': reverse('send_reg_verification'),
            'login': reverse('login'),
            'has_tfa': False,
            'email_recent': reverse('recent_key'),
            'email_verify': reverse('verify_key'),
            'email_resend': reverse('resend_key'),
            'email_remove': reverse('remove_key'),

            'add_payment': reverse_lazy('add_payment'),
            'get_payments': reverse_lazy('get_payments'),
            'remove_payment': reverse_lazy('remove_payment'),
        }
    )



@api_view(['GET'])
@not_authenticated()
def register(request):
    """
        This is the get method for the register view
        that is used to render the register page
    """

    # -- Render the register page
    return render(
        request, 
        'register.html', 
        context={
            'providers': format_providers(),
            'token': reverse('token'),
            'get_token': reverse('get_token'),
            'register': reverse('send_reg_verification'),
            'login': reverse('login'),
            'email_recent': reverse('recent_key'),
            'email_verify': reverse('verify_key'),
            'email_resend': reverse('resend_key'),
            'email_remove': reverse('remove_key'),

            'add_payment': reverse_lazy('add_payment'),
            'get_payments': reverse_lazy('get_payments'),
            'remove_payment': reverse_lazy('remove_payment'),
        }
    )



@api_view(['POST'])
@not_authenticated()
@required_headers(['Authorization'])
def validate_token(request, headers):
    """
        This view is used to validate a token
        Which is the standardaized way of authenticating
        with our app.
    """

    # Pass the header to the authenication function
    user = authenticate_key(headers['Authorization'])
    if user[0] is None: return invalid_response('Invalid Authorization header')

    # -- Log the user in
    request._request.user = user[0]
    request._request.method = 'GET'
    dj_login(request._request, user[0])

    # -- Add to the login history
    Statistics.log('accounts', 'login')
    user[0].ensure()
    LoginHistory.objects.create(
        member=user[0],
        ip=request.META['REMOTE_ADDR'],
        method=user[1]
    )

    # -- Check if the user has security preferences
    if user[0].security_preferences is None:
        user[0].security_preferences = SecurityPreferences.objects.create()
        user[0].save()

    # -- Inform the user that they have logged in
    if user[0].security_preferences.email_on_login:
        send_template_email(user[0], 'login_success')

    # -- Return the user to the member profile
    return success_response('Successfully logged in')



@api_view(['POST'])
@not_authenticated()
@required_data(['emailorusername', 'password'])
def get_token(request, data):
    """
        This view is responsible for generating a token
        for the user depending on the requirements
        of their login.
    """

    # -- Probably an email
    if data['emailorusername'].find('@') != -1:
        try: user = Member.objects.get(email=data['emailorusername'].lower())
        except Member.DoesNotExist: return invalid_response('Invalid credentials')

    # -- Probably a username
    else:
        try: user = Member.objects.get(username=data['emailorusername'].lower())
        except Member.DoesNotExist: return invalid_response('Invalid credentials')


    # -- Authenticate the user
    user.ensure()
    if not user.check_password(data['password']):
        if user.security_preferences.email_on_login:
            send_template_email(user, 'login_failed')
        return invalid_response('Invalid credentials')

    # -- Check if the user requires MFA
    if user.security_preferences.require_mfa_on_login:
        # -- Check what type of MFA is required
        if user.tfa_secret is not None:

            # -- Check if the user has provided a TOTP
            totp = request.data.get('totp', None)
            if totp is not None:
                if user.verify_mfa(totp):
                    return success_response('Successfully logged in', { 
                        'mode': 'none',
                        'token': generate_key(user)
                    })
                else: return invalid_response('Invalid TOTP')

            # -- TOTP, we need to send a key
            Statistics.log('accounts', 'mfa_totp')
            return success_response(
                'MFA required', 
                { 'mode': 'totp', }, 
                status.HTTP_202_ACCEPTED
            )
        
        else: 
            # -- EMail, we need to send a key
            token = f'EMAIL:{secrets.token_urlsafe(32)}'
            def callback(member):
                generate_key(member, token)

            keys = add_key(user, user.email, callback=callback)
            send_email(keys[0])

            # -- Return the response
            return success_response('MFA required', { 
                    'mode': 'mfa', 
                    'resend': keys[1],
                    'verify': keys[2],
                    'token': token,
                }, status.HTTP_202_ACCEPTED
            )

    
    else: return success_response(
        'Successfully logged in',
        { 
            'mode': 'none',
            'token': generate_key(user)
        }
    )



@api_view(['POST', 'GET'])
@authenticated()
def logout(request):
    """
        This view is used to logout the user
    """
    # -- Log the user out
    request._request.method = 'GET'
    request._request.user = request.user
    dj_logout(request._request)
    Statistics.log('accounts', 'logout')

    return success_response('Successfully logged out')