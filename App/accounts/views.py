from django.shortcuts import render, redirect
from django.contrib.auth import logout as dj_logout, login as dj_login, authenticate
from django.urls import reverse_lazy, reverse
from django.contrib.auth.hashers import check_password, make_password
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from accounts.create import create_account_oauth
from .auth_lib import authenticate_key, generate_key
from .oauth.oauth import format_providers, get_oauth_data
from .models import Member
from .email.email import send_email



"""
    This view is used to get a token
    aka, login
"""
@api_view(['GET'])
def login(request):
    # -- Make sure that the user isint already logged in
    if request.user.is_authenticated:
        return redirect(
            reverse_lazy('member_profile', urlconf='accounts.urls')
        )

    # -- Construct the context
    context = {
        'providers': format_providers(),

        'token': reverse('token'),
        'get_token': reverse('get_token'),
        'register': reverse('register'),
        'login': reverse('login'),

        # -- Email
        'email_recent': reverse('recent'),
        'email_verify': reverse('verify'),
        'email_resend': reverse('resend'),
    }

    # -- Render the login page
    return render(
        request, 
        'login.html', 
        context=context
    )




"""
    This function will be used to register a 
    user, the client can provide the oauth data
    or the email and password
"""
@api_view(['POST', 'GET'])
def register(request):
    match request.method:
        case 'POST': return register_post(request)
        case 'GET': return register_get(request)

    return JsonResponse({
        'message': 'Invalid method'
    }, status=status.HTTP_400_BAD_REQUEST)


def register_post(request):
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
    if 'email' not in request.data or 'password' not in request.data or 'username' not in request.data:
        return JsonResponse({
            'message': 'Missing email or password or username',
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)

    # -- Get the email and password
    email = request.data['email'].lower()
    password = request.data['password']
    username = request.data['username'].lower()

    
    # -- If we have an oauth token
    if oauth_token is not None:
        new_member = create_account_oauth(oauth_token, email, username, password)
        
        # -- If the account was created successfully
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
    else: return send_email(email, username, password)

        


"""
    This is the get method for the register view
    that is used to render the register page
"""
def register_get(request):
    # -- Make sure that the user isint already logged in
    if request.user.is_authenticated:
        return redirect(
            reverse_lazy('member_profile', urlconf='accounts.urls')
        )

    # -- Construct the context
    context = {
        'providers': format_providers(),

        'token': reverse('token'),
        'get_token': reverse('get_token'),
        'register': reverse('register'),
        'login': reverse('login'),

        # -- Email
        'email_recent': reverse('recent'),
        'email_verify': reverse('verify'),
        'email_resend': reverse('resend'),
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
        try: user = Member.objects.get(username=emailorusername.lower())
        except Member.DoesNotExist:
            return JsonResponse({
                'message': 'Invalid credentials',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)

    print(password)
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




@api_view(['GET'])
def profile(request):
    print(request.user)

    # -- Make sure that the user is logged in
    if not request.user.is_authenticated:
        return redirect('login')

    # -- Construct the context
    context = {
        'user': request.user,
    }

    # -- Render the profile page
    return render(
        request, 
        'profile.html', 
        context=context
    )




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
