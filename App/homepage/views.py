from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from django.conf import settings

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
        'description': 'You have successfully enabled MFA on your account'
    }

    return render(
        request, 
        'email/base.html', 
        context
    )