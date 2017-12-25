from django.db import models
from django.contrib import auth
import secrets

auth.signals.user_logged_in.disconnect(auth.models.update_last_login)


class User(models.Model):
    email = models.EmailField(primary_key=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True

    @property
    def email_root(self):
        return self.email.split('@')[0]


class Token(models.Model):

    email = models.EmailField()
    uid = models.CharField(default=secrets.token_urlsafe, max_length=100)
