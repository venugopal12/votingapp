from django.urls import path
from accounts import views

urlpatterns = [
    path(
        'send_login_email',
        views.SendLoginEmail.as_view(),
        name='send_login_email'
    ),
    path('login', views.Login.as_view(), name='login'),
]
