from django.views.generic import View, FormView
from django.shortcuts import render, redirect
from django.db.models import Sum
from pygal import Pie
from pygal.style import Style
from polls.models import Poll, Choice
from polls.forms import NewPollForm


class HomeView(FormView):
    template_name = 'home.html'
    form_class = NewPollForm

    def form_valid(self, form):
        form.save()
        return redirect('poll', uid=form.poll.uid)

    def get_context_data(self, **kwargs):
        kwargs['popular'] = Poll.objects.annotate(
            total_votes=Sum('choice__votes')
        ).order_by('-total_votes')[:10]
        return super().get_context_data(**kwargs)


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

    colors = (
        '#f75f5f', '#4fef44', '#44efe5',
        '#c844ef', '#ef4488', '#e8f562',
        '#f5b762', '#6286f5'
    )
    custom_style = Style(
        background='transparent',
        plot_background='#2b2b2b',
        foreground='white',
        foreground_strong='white',
        foreground_subtle='white',
        transition='100ms ease-in',
        opacity_hover='.25',
        tooltip_font_size=22,
        colors=colors
    )

    def get(self, request, uid):
        poll = Poll.objects.annotate(
            total_votes=Sum('choice__votes')
        ).get(uid=uid)

        pie_chart = Pie(style=self.custom_style)
        choices = poll.choice_set.all().order_by('-votes')
        for i, choice in enumerate(choices):
            pie_chart.add(choice.text, choice.votes)
            choice.color = self.colors[i]

        poll.choices = choices

        return render(request, 'results.html', {
            'poll': poll,
            'chart': pie_chart.render_data_uri()
        })
