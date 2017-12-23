from django.views.generic import View
from django.shortcuts import redirect, reverse
from django.core.mail import send_mail
from django.contrib import auth, messages
from accounts.models import Token


class SendLoginEmail(View):

    def post(self, request):
        email = request.POST['email']
        token = Token.objects.create(email=email)
        login_url = request.build_absolute_uri(
            reverse('login') + '?uid=' + token.uid
        )

        send_mail(
            'Your login for Mini Votes',
            f'Use this link to log in: {login_url}',
            'noreply@vote.miniscruff.com',
            [email]
        )
        messages.success(
            request,
            f'Email sent to {email}'
        )
        return redirect('/')


class Login(View):

    def get(self, request):
        user = auth.authenticate(uid=request.GET['uid'])
        if user is not None:
            auth.login(request, user)
            messages.success(
                request,
                f'Welcome {user.email_root}!'
            )
        return redirect('/')
