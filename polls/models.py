from django.db import models
import secrets


class Poll(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    uid = models.CharField(
        primary_key=True,
        default=secrets.token_urlsafe,
        max_length=40
    )


class Choice(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(blank=False, max_length=200)
    votes = models.IntegerField(default=0)
