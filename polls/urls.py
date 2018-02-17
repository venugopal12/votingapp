from django.urls import path
from polls import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('poll/<uid>', views.PollView.as_view(), name='poll'),
    path('poll/<uid>/results', views.ResultsView.as_view(), name='results'),
    path('api/v1/polls', views.PollsListAPIView.as_view(), name='api_polls'),
    path(
        'api/v1/poll/<uid>',
        views.PollDetailAPIView.as_view(),
        name='api_poll_detail'
    ),
]
