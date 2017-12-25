from django.test import TestCase
from django.core.exceptions import ValidationError
from polls.models import Poll, Choice, short_urltoken

from datetime import datetime, timedelta, timezone


class ModelsTest(TestCase):

    def test_short_url_token_is_unique(self):
        self.assertNotEqual(
            short_urltoken(),
            short_urltoken()
        )


class PollModelTest(TestCase):

    def test_can_not_save_empty_text(self):
        poll = Poll(text='')
        with self.assertRaises(ValidationError):
            poll.full_clean()

    def test_pub_date_is_now(self):
        poll = Poll.objects.create(text='text')
        self.assertTrue(
            datetime.now(timezone.utc) - poll.pub_date < timedelta(seconds=0.2)
        )

    def test_uid_is_primary_key(self):
        poll = Poll.objects.create(text='text')
        self.assertEqual(poll.pk, poll.uid)


class ChoiceModelTest(TestCase):

    def test_choice_is_related_to_poll(self):
        poll = Poll.objects.create(text='text')
        choice = Choice.objects.create(poll=poll, text='')
        self.assertIn(choice, poll.choice_set.all())

    def test_requires_poll(self):
        choice = Choice(text='text')
        with self.assertRaises(ValidationError):
            choice.full_clean()

    def test_can_not_save_empty_text(self):
        poll = Poll.objects.create(text='text')
        choice = Choice(poll=poll, text='')
        with self.assertRaises(ValidationError):
            choice.full_clean()

    def test_votes_start_at_zero(self):
        poll = Poll.objects.create(text='text')
        choice = Choice.objects.create(poll=poll, text='text')
        self.assertEqual(choice.votes, 0)
