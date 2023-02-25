from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['POST'])
def submit_streamer_app(request, streamer_form_data):
    # -- Make sure that the user isint already logged in
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': 'You are not logged in'
        }, status=status.HTTP_400_BAD_REQUEST)
