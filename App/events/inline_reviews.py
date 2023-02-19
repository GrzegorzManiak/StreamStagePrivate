from .forms import ReviewUpdateForm, ReviewCreateForm
from django.shortcuts import redirect
from .models import EventReview

def handle(request, event):
    # TODO: Check if user has watched event.
    if not request.user.is_authenticated:
        return None

    # checking if user has already reviewed this event
    existing_review = EventReview.objects.filter(author=request.user,event=event)
    if existing_review:
        return None
    
    form = ReviewCreateForm(request.POST or None)

    if request.POST and form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.event = event
        form.save()
        
        return redirect('event_view', event.event_id)
    
    return form