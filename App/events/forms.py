from django import forms
from .models import Event
 
# creating a form
class EventCreateForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Event
 
        # specify fields to be used
        fields = [
            'title', 
            'description', 
            'categories', 
            'showings', 
            'media',
        ]

class EventUpdateForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Event
 
        # specify fields to be used
        fields = [
            'title', 
            'description', 
            'categories', 
            'showings', 
            'media',
        ]

class EventDeleteForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Event

        # specify fields to be used
        fields = []