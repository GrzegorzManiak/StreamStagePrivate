import secrets
import pyotp

from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.decorators import api_view

from django_countries.fields import CountryField
from timezone_field import TimeZoneField
from StreamStage.mail import send_template_email
from accounts.com_lib import authenticated, error_response, invalid_response, required_data, success_response, is_admin

from accounts.oauth.oauth import get_all_oauth_for_member, format_providers
from accounts.email.verification import add_key, send_email
from accounts.models import LoginHistory, oAuth2


@api_view(['GET'])
@is_admin()
def site_panel(request):
    """
        This is the main site control panel
        allowing admins to manage the site
    """
    # -- Render the site panel
    return render(
        request,
        'admin/site_panel.html',
        context={
        }
    )
