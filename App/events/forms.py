from django import forms
from .models import Event, EventReview, Category, EventMedia, EventTrailer
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

    title = forms.CharField(widget=forms.Textarea(attrs={'name':'title', 'rows':1, 'cols':100}))
    description = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':10, 'cols':100}))
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)

# Deleting an Event
class EventDeleteForm(forms.ModelForm):
 
    class Meta:
        model = Event
        fields = []

                            # ***************
                            # *** Reviews *** 
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
    title = forms.CharField(label='', widget=forms.Textarea(attrs={'name':'', 'rows':1, 'cols':100, 'placeholder':'Title'}))
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'name':'body', 'rows':4, 'cols':100, 'placeholder':'Review'}))
    rating = forms.CharField(label='')


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
    title = forms.CharField(widget=forms.Textarea(attrs={'name':'title', 'rows':1, 'cols':100}))
    body = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':4, 'cols':100}))

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