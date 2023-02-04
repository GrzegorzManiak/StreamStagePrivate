from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse_lazy, reverse
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

from accounts.create import create_account_oauth

from .auth_lib import authenticate_key
from .oauth.oauth import format_providers, check_oauth_key, get_oauth_data

# class MemberSignUpView(CreateView):
#     form_class = MemberCreationForm
#     template_name = 'signup.html'

#     def post(self, request, *args, **kwargs):
#         form = MemberCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             signup_user = Member.objects.get(username=username)
#             member_group = Group.objects.get(name='Member')
#             member_group.user_set.add(signup_user)
#             return redirect('auth')
#         else:
#             return render(request, self.template_name, {'form' : form })



"""
    This view is used to get a token
    aka, login
"""
@api_view(['GET'])
def login(request):
    # -- Make sure that the user isint already logged in
    if request.user.is_authenticated:
        return reverse_lazy('member_profile')

    # -- Construct the context
    context = {
        'providers': format_providers(),

        'token': reverse('token'),
        'get_token': reverse('get_token'),
        'register': reverse('register'),
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
    email = request.data['email']
    password = request.data['password']
    username = request.data['username']

    
    # -- If we have an oauth token
    if oauth_token is not None:
        new_member = create_account_oauth(oauth_token, email, username, password)
        
        # -- If the account was created successfully
        if isinstance(new_member, JsonResponse):
            return new_member

        return JsonResponse({
            'message': 'Account created successfully',
            'status': 'success'
        }, status=status.HTTP_201_CREATED)

        


    
def register_get(request):
    # -- Make sure that the user isint already logged in
    if request.user.is_authenticated:
        return redirect('member_profile')
        




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
    if len(auth_header) < 10 or len(auth_header) > 100:
        return JsonResponse({
            'message': 'Invalid Authorization header'
        }, status=status.HTTP_400_BAD_REQUEST)


    # Pass the header to the authenication function
    user = authenticate_key(auth_header)

    if user is not None:
        # -- Log the user in
        login(request, user)

        # -- Return a success message
        return JsonResponse({
            'message': 'Logged in successfully'
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
@api_view(['GET'])
def get_token(request):
    pass