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
    total_votes = models.IntegerField(default=0)


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(blank=False, max_length=200)
    _votes = models.IntegerField(default=0)

    @property
    def votes(self):
        return self._votes

    def vote(self):
        self._votes += 1
        self.save()
        self.poll.total_votes += 1
        self.poll.save()

    class Meta:
        ordering = ('id',)
