from django import forms
from .models import Event, EventReview, EventShowing, EventMedia, EventTrailer
                                        # ***************
                                        # *** Events  ***                                        # ***************
                                        # *************** 

# Updating an Event
class EventUpdateForm(forms.ModelForm):
 
    class Meta:
        model = Event
        exclude = [
            "event_id",
            "broadcaster",
            "approved",
            "contributors",
            "primary_media_idx"
        ]

# Deleting an Event
class EventDeleteForm(forms.ModelForm):
 
    class Meta:
        model = Event
        fields = []


                                        # ****************
                                        # *** Showings ***                                        # ***************
                                        # ****************


class ShowingCreateForm(forms.ModelForm):
    
    class Meta:
        model = EventShowing
        fields = [
            'time', 
            'venue', 
            'city',
            'country'
        ]

        widgets = {
            'time': forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%H:%M %d/%m/%Y')
        }

class ShowingUpdateForm(forms.ModelForm):
    
    class Meta:
        model = EventShowing
        fields = [
            'time', 
            'venue', 
            'city',
            'country'
        ]

class ShowingDeleteForm(forms.ModelForm):
    
    class Meta:
        model = EventShowing
        fields = []


                                        # ***************
                                        # *** Reviews ***                                        # ***************
                                        # ***************

# Creating an Event Review
class ReviewCreateForm(forms.ModelForm):
 
    class Meta:
        model = EventReview
        fields = [
            'title', 
            'body', 
            'rating'
        ]

# Updating an Event Review
class ReviewUpdateForm(forms.ModelForm):
 
    class Meta:
        model = EventReview
        exclude = [
            'event',
            'review_id',
            'author',
            'event',
            'created',
            'updated',
            'likes',
            'likers'
        ]

# Deleting an Event Review
class ReviewDeleteForm(forms.ModelForm):
 
    class Meta:
        model = EventReview
        fields = []

                                        # ***************
                                        # **** Media ****                                        # ***************
                                        # ***************

# Creating Media
class MediaCreateForm(forms.ModelForm):
    class Meta:
        model= EventMedia
        exclude = ['event']

# Updating Media
class MediaUpdateForm(forms.ModelForm):
    class Meta:
        model= EventMedia
        exclude = ['event']

# Deleting Event Media
class MediaDeleteForm(forms.ModelForm):
 
    class Meta:
        model = EventMedia
        fields = []

                                        # **************
                                        # ** Trailers **                                        # ***************
                                        # **************

# Creating Trailer
class TrailerCreateForm(forms.ModelForm):
    class Meta:
        model= EventTrailer
        exclude = ['event']

# Updating Trailer
class TrailerUpdateForm(forms.ModelForm):
    class Meta:
        model= EventTrailer
        exclude = ['event']

# Deleting Trailer
class TrailerDeleteForm(forms.ModelForm):
 
    class Meta:
        model = EventTrailer
        fields = []