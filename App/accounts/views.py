from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import Group
from .forms import MemberCreationForm
from .models import Member #, StreamerProfile

from .auth_lib import authenticate_key
from .oauth.oauth import format_providers

class MemberSignUpView(CreateView):
    form_class = MemberCreationForm
    template_name = 'signup.html'

    def post(self, request, *args, **kwargs):
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = Member.objects.get(username=username)
            member_group = Group.objects.get(name='Member')
            member_group.user_set.add(signup_user)
            return redirect('auth')
        else:
            return render(request, self.template_name, {'form' : form })



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
        'providers': format_providers()
    }

    # -- Render the login page
    return render(
        request, 
        'login.html', 
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