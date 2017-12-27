from django.urls import path
from polls import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('new', views.NewPollView.as_view(), name='new_poll'),
    path('poll/<uid>', views.PollView.as_view(), name='poll'),
    path('poll', views.PollView.as_view(), name='poll'),
    path('poll/<uid>/results', views.ResultsView.as_view(), name='results'),
    path('vote', views.VoteView.as_view(), name='vote'),
]
