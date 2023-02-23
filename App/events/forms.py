from django import forms
from .models import Event, EventReview, Category, EventShowing

                                        # ***************
                                        # *** Events  ***                                        # ***************
                                        # *************** 
# Creating an Event

class CategoryMC(forms.ModelMultipleChoiceField):
    def label_from_instance(self, category):
        return category.name
    
# class MediaMC(forms.ModelMultipleChoiceField):
#     def label_from_instance(self, media):
#         return media.picture

class EventApplyForm(forms.ModelForm):
 
    class Meta:
        model = Event
 
        fields = [
            'title', 
            'description', 
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
            "streamer",
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
class EventShowingCreate(forms.ModelForm):
    
    class Meta:
        model = EventShowing
 
        fields = [
            'time', 
            'venue', 
            'city',
            'country'
        ]

class EventShowingUpdate(forms.ModelForm):
    
    class Meta:
        model = EventShowing
 
        fields = [
            'time', 
            'venue', 
            'city',
            'country'
        ]

class EventShowingDelete(forms.ModelForm):
    
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
            'review_id',
            'author',
            'event',
            'created',
            'updated',
            'likes'
        ]

# Deleting an Event Review
class ReviewDeleteForm(forms.ModelForm):
 
    class Meta:
        model = EventReview

        fields = []