from django.views.generic import View
from django.shortcuts import redirect
from django.core.mail import send_mail


class SendLoginEmail(View):

    def post(self, request):
        email = request.POST['email']
        send_mail(
            'Your login for Mini Votes',
            'Use this link to log in: ',
            'noreply@vote.miniscruff.com',
            [email]
        )
        return redirect('/')
