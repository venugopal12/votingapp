from django.views.generic import View, FormView
from django.shortcuts import render, redirect
from django.db.models import Sum
from polls.models import Poll, Choice
from polls.forms import NewPollForm


class HomeView(FormView):
    template_name = 'home.html'
    form_class = NewPollForm

    def form_valid(self, form):
        form.save()
        return redirect('poll', uid=form.poll.uid)


class PollView(View):

    def get(self, request, uid):
        poll = Poll.objects.get(uid=uid)
        return render(request, 'poll.html', {'poll': poll})

    def post(self, request, uid):
        poll = Poll.objects.get(uid=uid)
        choice = Choice.objects.get(id=request.POST['choice_id'])
        choice.votes += 1
        choice.save()

        return redirect('results', uid=poll.uid)


class ResultsView(View):

    def get(self, request, uid):
        poll = Poll.objects.annotate(
            total_votes=Sum('choice__votes')
        ).get(uid=uid)
        return render(request, 'results.html', {'poll': poll})
