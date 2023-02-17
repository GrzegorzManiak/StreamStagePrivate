from django import forms
from .models import Event, EventReview

                                        # ***************
                                        # *** Events  ***                                        # ***************
                                        # *************** 
# Creating an Event
class EventCreateForm(forms.ModelForm):
 
    class Meta:
        model = Event
 
        fields = [
            'title', 
            'description', 
            'categories', 
            'showings', 
            'media',
        ]

# Updating an Event
class EventUpdateForm(forms.ModelForm):
 
    class Meta:
        model = Event
 
        fields = [
            'title', 
            'description', 
            'categories', 
            'showings', 
            'media',
        ]

# Deleting an Event
class EventDeleteForm(forms.ModelForm):
 
    class Meta:
        model = Event

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
 
        fields = [
            'title', 
            'body', 
            'rating'
        ]

# Deleting an Event Review
class ReviewDeleteForm(forms.ModelForm):
 
    class Meta:
        model = EventReview

        fields = []