from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from polls.models import Poll, Choice


class HomeView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'dashboard.html')
        return render(request, 'home.html')


class NewPollView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(
                request,
                'You need to be logged in to create a poll'
            )
            return redirect('/')
        return render(request, 'new_poll.html')


class PollView(View):

    def get(self, request, uid):
        return render(request, 'poll.html')

    def post(self, request):
        text = request.POST['text']
        poll = Poll.objects.create(text=text)

        for choice in request.POST.getlist('choices'):
            Choice.objects.create(text=choice, poll=poll)

        return redirect(f'/poll/{poll.uid}')
