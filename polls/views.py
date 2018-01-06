from django.views.generic import View
from django.shortcuts import render, redirect
from polls.models import Poll, Choice


class HomeView(View):

    def get(self, request):
        return render(request, 'home.html')

    def post(self, request):
        text = request.POST['text']
        poll = Poll.objects.create(text=text)

        for choice in request.POST.getlist('choices'):
            Choice.objects.create(text=choice, poll=poll)

        return redirect(f'/poll/{poll.uid}')


class PollView(View):

    def get(self, request, uid):
        poll = Poll.objects.get(uid=uid)
        return render(request, 'poll.html', {'poll': poll})

    def post(self, request, uid):
        poll = Poll.objects.get(uid=uid)
        choice = Choice.objects.get(id=request.POST['choice_id'])
        choice.vote()

        return redirect(f'/poll/{poll.uid}/results')


class ResultsView(View):

    def get(self, request, uid):
        poll = Poll.objects.get(uid=uid)
        return render(request, 'results.html', {'poll': poll})
