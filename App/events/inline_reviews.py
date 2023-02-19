from .forms import ReviewUpdateForm, ReviewCreateForm
from django.shortcuts import redirect
from .models import EventReview

def handle(request, event):
    context = {
        'new_review_form': None
    }

    # TODO: Check if user has watched event.
    if not request.user.is_authenticated:
        return context
        
    # temporary override so we can add multiple reviews
    # per user
    override = request.GET.get('review_override', 'n')
    if override == 'n':
        # checking if user has already reviewed this event
        existing_review = EventReview.objects.filter(author=request.user,event=event)
        if existing_review:
            return context
    
    form = ReviewCreateForm(request.POST or None)

    if request.POST and form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.event = event
        form.save()

        return context 
    
    context['new_review_form'] = form

    return context