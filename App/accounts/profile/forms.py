from django import forms
from django.urls import reverse
from django.apps import apps
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework import status

def beautify_form_errors(dict) -> str or None:
    error = ''
    
    for key, value in dict.items():
        error += f'{key}: {value[0]} \n'

    return error

# -- Change details form
class ChangeBasicDetailsForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('accounts', 'Member')
        fields = [
            'profile_pic',
            'username',
            'first_name',
            'last_name',
            'description',
            'country',
            'time_zone',
        ]
        
@api_view(['POST'])
def change_basic_details(request):
    # -- Make sure that the user is logged in
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'You are not logged in',
        }, status=status.HTTP_401_UNAUTHORIZED)

    # -- Get the form
    form = ChangeBasicDetailsForm(
        request.POST, 
        request.FILES, 
        instance=request.user
    )

    form.full_clean()   
    
    # -- Check if the form is valid
    if form.is_valid():
        form.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Your details have been updated',
        }, status=status.HTTP_200_OK)

    # -- Return the errors
    return JsonResponse({
        'status': 'error',
        'message': beautify_form_errors(form.errors),
    }, status=status.HTTP_400_BAD_REQUEST)



def get_change_basic_details_form(member):

    # -- Get the form for the user    
    return {
        'endpoint': reverse('edit_basic_details'),
        'form': ChangeBasicDetailsForm(instance=member),
    }




def compile_objects(member):
    return {
        'profile': get_change_basic_details_form(member)
    }