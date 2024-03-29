from django import forms
from django.db import models
from .models import *
from StreamStage.utilities import CategoryMC
from events.models import Category

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
            'biography'
        ]

    # less work doing it this way than generating a Broadcaster with code i think.
    submission_statement = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':5, 'cols':32, 'placeholder': 'TITLE'}))
    
class EventAppForm(forms.ModelForm):
    class Meta:
        model = Event

        fields = [
            'broadcaster',
            'title', 
            'description', 
            'categories',
            'over_18s',
            # 'stream_price'
        #    'showings', 
        #    'media',
        ]
    
    def __init__(self, *args, **kwargs):
        streamer = kwargs.pop('streamer','')
        super(EventAppForm, self).__init__(*args, **kwargs)

        # Ensure only this user's broadcasters can be selected.
        
        user_broadcasters = Broadcaster.objects.filter(streamer=streamer)
        most_recent_broadcaster = user_broadcasters.last()

        self.fields['broadcaster'] = forms.ModelChoiceField(queryset=user_broadcasters, initial=most_recent_broadcaster)
        
        # self.fields['categories'] = CategoryMC(
        #      queryset=Category.objects.all(),
        #      widget=forms.CheckboxSelectMultiple
        #  )
