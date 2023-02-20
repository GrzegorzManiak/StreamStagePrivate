from django.contrib.auth import login as dj_login, logout as dj_logout
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models.functions import Lower

from accounts.auth_lib import authenticate_key, generate_key
from accounts.email.verification import send_email, add_key
from accounts.models import Member
from accounts.oauth.oauth import format_providers, get_oauth_data


"""
    This view is used to get a token
    aka, login
"""
@api_view(['GET'])
def login(request):
    # -- Make sure that the user isint already logged in
    if request.user.is_authenticated:
        return redirect(
            reverse_lazy('member_profile')
        )

    # -- Construct the context
    context = {
        'providers': format_providers(),

        'token': reverse('token'),
        'get_token': reverse('get_token'),
        'register': reverse('send_reg_verification'),
        'login': reverse('login'),

        # -- Security
        'has_tfa': False,

        # -- Email
        'email_recent': reverse('recent_key'),
        'email_verify': reverse('verify_key'),
        'email_resend': reverse('resend_key'),
    }
    
    # -- Render the login page
    return render(
        request, 
        'login.html', 
        context=context
    )



"""
    This is the get method for the register view
    that is used to render the register page
"""
@api_view(['GET'])
def register(request):
    # -- Make sure that the user isint already logged in
    if request.user.is_authenticated:
        return redirect(
            reverse_lazy('member_profile')
        )

    # -- Construct the context
    context = {
        'providers': format_providers(),

        'token': reverse('token'),
        'get_token': reverse('get_token'),
        'register': reverse('send_reg_verification'),
        'login': reverse('login'),

        # -- Email
        'email_recent': reverse('recent_key'),
        'email_verify': reverse('verify_key'),
        'email_resend': reverse('resend_key'),
    }

    # -- Render the register page
    return render(
        request, 
        'register.html', 
        context=context
    )




"""
    This view is used to validate a token
    Which is the standardaized way of authenticating
    with our app.
"""
@api_view(['POST'])
def validate_token(request):
    # -- Make sure that the user isint already logged in
    if request.user.is_authenticated:
        return JsonResponse({
            'message': 'You are already logged in'
        }, status=status.HTTP_400_BAD_REQUEST)

    # -- Make sure we have the Authorization header 
    if 'Authorization' not in request.headers:
        return JsonResponse({
            'message': 'Missing Authorization header'
        }, status=status.HTTP_400_BAD_REQUEST)

    # -- Get the authorization header
    auth_header = request.headers['Authorization']

    # -- Make sure the header is not too long or too short
    if len(auth_header) < 10 or len(auth_header) > 150:
        return JsonResponse({
            'message': 'Invalid Authorization header'
        }, status=status.HTTP_400_BAD_REQUEST)


    # Pass the header to the authenication function
    user = authenticate_key(auth_header)

    if user is not None:
        # -- Log the user in
        request._request.user = user
        request._request.method = 'GET'
        dj_login(request._request, user)

        # -- Return the user to the member profile
        return JsonResponse({
            'message': 'Successfully logged in',
            'status': 'success'
        }, status=status.HTTP_200_OK)

    
    # -- Otherwise return an error message
    return JsonResponse({
        'message': 'Invalid Authorization header'
    }, status=status.HTTP_400_BAD_REQUEST)
    



"""
    This view is responsible for generating a token
    for the user depending on the requirements
    of their login.
"""
@api_view(['POST'])
def get_token(request):
    # -- Make sure that the user isint already logged in
    if request.user.is_authenticated:
        return JsonResponse({
            'message': 'You are already logged in'
        }, status=status.HTTP_400_BAD_REQUEST)

    # -- Get the json data
    if 'emailorusername' not in request.data or 'password' not in request.data:
        return JsonResponse({
            'message': 'Missing email or password',
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)

    # -- Get the email and password
    emailorusername = request.data['emailorusername'].lower()
    password = request.data['password']


    # -- Probably an email
    if emailorusername.find('@') != -1:
        try: user = Member.objects.get(email=emailorusername.lower())
        except Member.DoesNotExist:
            return JsonResponse({
                'message': 'Invalid credentials',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)

    # -- Probably a username
    else:
        # -- We need to find the user by username even if they are in different cases
        try: user = Member.objects.get(cased_username=emailorusername)
        except Member.DoesNotExist:
            return JsonResponse({
                'message': 'Invalid credentials',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)

    # -- Authenticate the user
    if not user.check_password(password):
        return JsonResponse({
            'message': 'Invalid credentials',
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)

    # -- Generate the token for the user
    token = generate_key(user)

    return JsonResponse({
        'message': 'Successfully logged in',
        'token': token,
        'status': 'success'
    }, status=status.HTTP_200_OK)



"""
    This view is used to logout the user
"""
@api_view(['POST', 'GET'])
def logout(request):
    match request.method:
        case 'POST': return logout_post(request)
        case 'GET': return logout_get(request)

    return JsonResponse({
        'message': 'Invalid method'
    }, status=status.HTTP_400_BAD_REQUEST)


def logout_post(request):
    # -- Make sure that the user is logged in
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': 'You are not logged in'
        }, status=status.HTTP_400_BAD_REQUEST)

    # -- Log the user out
    request._request.method = 'GET'
    request._request.user = request.user
    dj_logout(request._request)

    # -- Return a success message
    return JsonResponse({
        'message': 'Successfully logged out',
        'status': 'success'
    }, status=status.HTTP_200_OK)


def logout_get(request):
    # -- Make sure that the user is logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # -- Log the user out
    request._request.method = 'GET'
    request._request.user = request.user
    dj_logout(request._request)

    # -- Return a success message
    return redirect('login')
