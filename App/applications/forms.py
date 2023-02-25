from django import forms
from django.db import models
from .models import *

                                        # ***************
                                        # *** Events  ***                                        # ***************
                                        # *************** 
# Creating an Event
class StreamerAppForm(forms.ModelForm):
    class Meta:
        model = StreamerApplication
        
        fields = [
            'submission_statement'
        ]

class BroadcasterAppForm(forms.ModelForm):
    class Meta:
        model = Broadcaster
        
        fields = [
            'handle',
            'name',
            'biography',
            'is_individual'
        ]

    # less work doing it this way than generating a Broadcaster with code i think.
    submission_statement = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':5, 'cols':32}))
    


