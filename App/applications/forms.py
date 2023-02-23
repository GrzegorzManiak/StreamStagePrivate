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
        
    XTRA_XTRA = forms.CharField()