from django.views.generic import View
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages


class SendLoginEmail(View):

    success_url = '/success/'
    success_message = 'Authentication Email sent'

    def post(self, request):
        email = request.POST['email']
        send_mail(
            'Your login for Mini Votes',
            'Use this link to log in: ',
            'noreply@vote.miniscruff.com',
            [email]
        )
        messages.success(
            request,
            f'Email sent to {email}'
        )
        return redirect('/')
