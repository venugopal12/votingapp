from django.views.generic import View
from django.shortcuts import render, redirect


class HomeView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'dashboard.html')
        return render(request, 'home.html')


class NewPollView(View):

    def get(self, request):
        return render(request, 'new_poll.html')


class PollView(View):

    def get(self, request, uid):
        return render(request, 'poll.html')

    def post(self, request):
        return redirect('/')
