from django.views.generic import View
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages
from accounts.models import Token


class SendLoginEmail(View):

    def post(self, request):
        email = request.POST['email']
        token = Token.objects.create(email=email)

        send_mail(
            'Your login for Mini Votes',
            f'Use this link to log in: http://testserver/login?token={token.uid}',
            'noreply@vote.miniscruff.com',
            [email]
        )
        messages.success(
            request,
            f'Email sent to {email}'
        )
        return redirect('/')
