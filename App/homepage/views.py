from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from django.conf import settings
from accounts.models import Member, Broadcaster
from StreamStage.templatetags.tags import cross_app_reverse
from events.models import EventReview, Event, Category

"""
    Main homepage view, first page a user sees when they visit the site
"""
@api_view(['GET'])
def index(request):

    # -- Get 3 random events
    featuerd = Event.objects.all().order_by('?')[:3]
    categories = Category.get_random_categories(10)
    categories_formatted = []

    for category in categories:
        categories_formatted.append({
            'category': category,
            'events': category.get_random_events(10)
        })
        

    context = {
        'is_admin': request.user.is_superuser,
        'base_url': settings.DOMAIN_NAME,
        'features': featuerd,
        'categories': categories_formatted,
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
        },
    )



@api_view(['GET'])
def broadcaster_profile(request, username):
    """
        This view is used to get a token
        aka, login
    """
   
    broadcaster = Broadcaster.objects.filter(
        handle__iexact=username
    ).first()
    
    if not broadcaster:
        return redirect('homepage_index')
    
    context = {
        'data': {
            'handle': broadcaster.handle,
            'background': broadcaster.banner.url,
            'avatar': broadcaster.profile_pic.url,
            'description': broadcaster.biography,
            'approved': broadcaster.approved,
            'is_you': False,
            'short_description': broadcaster.biography[:50] + '...' if len(broadcaster.biography) > 50 else broadcaster.biography,
            'name': broadcaster.name,
            'joined': broadcaster.created,
            'reviews': 0,
        },
        'api': {
            'get_reviews': cross_app_reverse('accounts', 'get_reviews'),
            'resend_verification': cross_app_reverse('accounts', 'resend_key'),
            'remove_verification': cross_app_reverse('accounts', 'remove_key'),
            'recent_verification': cross_app_reverse('accounts', 'recent_key'),
            'submit_report': reverse_lazy('submit_report'),
        }
    }

    if request.user.is_authenticated and broadcaster in request.user.get_authorized_broadcasters():
        context['edit_details_path'] = cross_app_reverse('accounts', 'broadcaster_panel') + "?bid=" + str(broadcaster.id)

    # -- Render the login page
    return render(
        request, 
        'profiles/broadcaster_profile.html', 
        context=context
    )
