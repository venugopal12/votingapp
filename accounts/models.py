from django.db import models
import random
import string

# 64 bits of entropy (26*2 letters + 10 digits + 2 special chars )
# same as youtube
UID_CHARS = string.ascii_letters + string.digits + '_-'
UID_LENGTH = 32


class Token(models.Model):

    def create_uid():
        return ''.join(random.choice(UID_CHARS) for _ in range(UID_LENGTH))

    email = models.EmailField()
    uid = models.CharField(default=create_uid, max_length=40)
