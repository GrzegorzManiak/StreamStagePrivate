
from django import forms
from accounts.models import Broadcaster


class BroadcasterUpdateForm(forms.ModelForm):
 
    class Meta:
        model = Broadcaster
        fields = [
            "biography",
            "handle",
            "name"
        ]
