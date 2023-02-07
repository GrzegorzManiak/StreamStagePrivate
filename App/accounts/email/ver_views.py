from accounts.oauth.oauth import link_oauth_account
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status

from ..models import Member

from .verification import (
    add_key,
    get_key,
    expire_key,
    get_key_by_resend_key,
    get_resend_key_by_key,
    remove_key,
    verify_key,
    send_email,
    regenerate_key,
    check_if_verified_recently,
)