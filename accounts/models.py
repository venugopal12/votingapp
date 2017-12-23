from django.db import models
from django.contrib import auth
import random
import string

# 64 bits of entropy (26*2 letters + 10 digits + 2 special chars )
# same as youtube
UID_CHARS = string.ascii_letters + string.digits + '_-'
UID_LENGTH = 32

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

    def create_uid():
        return ''.join(random.choice(UID_CHARS) for _ in range(UID_LENGTH))

    email = models.EmailField()
    uid = models.CharField(default=create_uid, max_length=40)
