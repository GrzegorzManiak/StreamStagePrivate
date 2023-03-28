from django import forms
from .models import Event, EventReview, Category, EventShowing
from StreamStage.utilities import CategoryMC

                                        # ***************
                                        # *** Events  ***                                        # ***************
                                        # *************** 
# Applying for an Event

# class MediaMC(forms.ModelMultipleChoiceField):
#     def label_from_instance(self, media):
#         return media.picture

class EventApplyForm(forms.ModelForm):

    class Meta:
        model = Event
 
        fields = [
            'title', 
            'description',
            'broadcaster',
            'over_18s',  
            'categories']

    categories = CategoryMC(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    # media = MediaMC(
    #     queryset=EventMedia.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )

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