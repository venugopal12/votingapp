from django.urls import path
from polls import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('new', views.NewPollView.as_view(), name='new_poll'),
]
