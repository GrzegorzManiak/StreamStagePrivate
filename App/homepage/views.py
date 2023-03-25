from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from django.conf import settings
from accounts.models import Member, Broadcaster
from StreamStage.templatetags.tags import cross_app_reverse
from events.models import EventReview

"""
    Main homepage view, first page a user sees when they visit the site
"""
@api_view(['GET'])
def index(request):

    context = {
        'is_admin': request.user.is_superuser,
        'base_url': settings.DOMAIN_NAME,
    }

    return render(
        request, 
        'main.html', 
        context
    )



@api_view(['GET'])
def email(request):
    
    context = {
        'email': 'test@greg.co',
        'support_email': 'adsfsadf@gmail.com',
        'year': '2023',
        'title': 'MFA Enabled',
        'description': 'You have successfully enabled MFA on your account',
        'email_id': '1234',
        'user': {
            'username': 'Greg',
        },
        'data': ['aJs3dD', '7jdG3d', '3dG3d', 'DF23ad', 'Sfg23H']
    }

    return render(
        request, 
        'email/mfa_disabled.html', 
        context
    )



@api_view(['GET'])
def user_profile(request, username):
    """
        This view is used to get a token
        aka, login
    """

    user = Member.objects.filter(
        username=username.lower()
    ).first()

    # -- Check if the user is logged in
    is_you = False
    if request.user.is_authenticated:   
        if request.user.username == username: is_you = True

    # -- TODO: 404 for private profiles and non-existent profiles

    # -- Last name privacy settings
    if user.security_preferences.public_name:
        lname = user.last_name
    else: lname = user.last_name[:1] + '.' if user.last_name else ''

    # -- Country privacy settings
    if user.security_preferences.public_country:
        country = user.country
    else: country = 'Private'

    # -- Total reviews
    reviews = EventReview.objects.filter(
        author=user
    ).all().count()

    # -- Render the login page
    return render(
        request, 
        'profiles/user_profile.html', 
        context={
            'data': {
                'name': user.cased_username,
                'background': user.get_profile_banner(),
                'avatar': user.get_profile_pic(),
                'description': user.description,
                'is_you': is_you,
                'short_description': user.description[:50] + '...' if len(user.description) > 50 else user.description,
                'fname': user.first_name,
                'lname': lname,
                'country': country,
                'joined': user.date_joined,
                'reviews': reviews,
            },
            'api': {
                'get_reviews': cross_app_reverse('accounts', 'get_reviews'),
                'resend_verification': cross_app_reverse('accounts', 'resend_key'),
                'remove_verification': cross_app_reverse('accounts', 'remove_key'),
                'recent_verification': cross_app_reverse('accounts', 'recent_key'),
                'submit_report': reverse_lazy('submit_report'),
            }
        }
    )



@api_view(['GET'])
def broadcaster_profile(request, username):
    """
        This view is used to get a token
        aka, login
    """
    # -- Render the login page
    return render(
        request, 
        'profiles/broadcaster_profile.html', 
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