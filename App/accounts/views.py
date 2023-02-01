from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView

from django.contrib.auth.models import Group
from .forms import MemberCreationForm
from .models import Member #, StreamerProfile

class MemberSignUpView(CreateView):
    form_class = MemberCreationForm
    template_name = 'registration/signup.html'

    def post(self, request, *args, **kwargs):
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = Member.objects.get(username=username)
            customer_group = Group.objects.get(name='Member')
            customer_group.user_set.add(signup_user)
            return redirect('login')
        else:
            return render(request, self.template_name, {'form' : form })


# class StreamerProfileSignUpView(CreateView):