from django.shortcuts import render, redirect

# Create your views here.

def apply_for_event(request):
    pass

def landing_url(request):
    user = request.user

    if user.is_authenticated:
        if user.is_staff:
            return render(request, "landing_staff.html")
        elif user.is_streamer:
            return render(request, "streamer_staff.html")


    return redirect('events:all_events')
