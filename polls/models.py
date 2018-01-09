from django.db import models
import secrets


def short_urltoken():
    return secrets.token_urlsafe(8)


class Poll(models.Model):
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    uid = models.CharField(
        default=short_urltoken,
        max_length=40
    )


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(blank=False, max_length=200)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ('id',)
