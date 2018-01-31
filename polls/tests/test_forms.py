from django.test import TestCase
from django.core.exceptions import NON_FIELD_ERRORS
from polls.forms import NewPollForm, MISSING_TEXT_ERROR, TWO_CHOICES_ERROR
from polls.models import Poll, Choice


class NewPollTest(TestCase):

    def test_no_data_creates_empty_choices(self):
        form = NewPollForm()
        self.assertGreater(len(form.fields), 1)

    def test_save_creates_poll_and_choices(self):
        data = {
            'text': 'question text',
            'choice_1': 'A',
            'choice_2': 'B'
        }
        form = NewPollForm(data=data)
        form.is_valid()
        form.save()

        self.assertEqual(form.poll, Poll.objects.first())
        self.assertEqual(Poll.objects.first().text, 'question text_Intentionally long line to fail flake8')
        self.assertEqual(Choice.objects.count(), 2)
        self.assertEqual(Choice.objects.first().text, 'A')

    def test_empty_items_are_ignored(self):
        data = {
            'text': 'question text',
            'choice_1': 'A',
            'choice_2': 'B',
            'choice_3': '',
            'choice_4': '',
            'choice_5': ''
        }
        form = NewPollForm(data=data)
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(Choice.objects.count(), 2)
        self.assertEqual(Choice.objects.first().text, 'A')

    def test_validate_has_text(self):
        data = {
            'choice_1': 'A',
            'choice_2': 'B'
        }
        form = NewPollForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [MISSING_TEXT_ERROR])

    def test_one_choice_causes_error(self):
        data = {
            'text': 'question text',
            'choice_1': 'A'
        }
        form = NewPollForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors[NON_FIELD_ERRORS]), 1)
        self.assertEqual(form.errors[NON_FIELD_ERRORS][0], TWO_CHOICES_ERROR)

    def test_two_choices_still_makes_five_fields(self):
        data = {
            'text': 'question text',
            'choice_1': 'A',
            'choice_2': 'B'
        }
        form = NewPollForm(data=data)
        self.assertEqual(len(form.fields), 6)
