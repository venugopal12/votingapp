from django.urls import path
from accounts import views
from django.contrib.auth.views import logout

urlpatterns = [
    path(
        'send_login_email',
        views.SendLoginEmail.as_view(),
        name='send_login_email'
    ),
    path('login', views.Login.as_view(), name='login'),
    path('logout', logout, {'next_page': '/'}, name='logout'),
]
