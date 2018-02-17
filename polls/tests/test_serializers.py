from collections import OrderedDict
from rest_framework.test import APITestCase
from polls.models import Poll, Choice
from polls.serializers import PollSerializer, ChoiceSerializer


class PollAPITest(APITestCase):

    def test_can_serialize_poll(self):
        poll = Poll.objects.create(text='My poll text')
        choice_0 = Choice.objects.create(text='First', poll=poll, votes=6)
        choice_1 = Choice.objects.create(text='Second', poll=poll, votes=17)
        serializer = PollSerializer(poll)
        self.assertDictEqual(serializer.data, {
            'id': poll.id,
            'uid': poll.uid,
            'text': 'My poll text',
            'pub_date': poll.pub_date.astimezone().isoformat(),
            'choices': [
                OrderedDict(
                    id=choice_0.id,
                    text=choice_0.text,
                    votes=choice_0.votes,
                ),
                OrderedDict(
                    id=choice_1.id,
                    text=choice_1.text,
                    votes=choice_1.votes,
                )
            ]
        })

    def test_can_create_poll_with_two_choices(self):
        serializer = PollSerializer(data={
            'text': 'My nested poll',
            'choices': [
                {'text': 'Choice A'},
                {'text': 'Choice B'},
            ]
        })
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.assertEqual(1, Poll.objects.count())
        poll = Poll.objects.first()
        self.assertEqual(poll.text, 'My nested poll')

        self.assertEqual(2, Choice.objects.count())
        choice = Choice.objects.first()
        self.assertEqual(choice.poll, poll)
        self.assertEqual(choice.text, 'Choice A')

    def test_invalid_poll_with_no_choices(self):
        serializer = PollSerializer(data={'text': 'My poll text'})
        self.assertFalse(serializer.is_valid())

    def test_invalid_poll_with_one_choice(self):
        serializer = PollSerializer(data={
            'text': 'My nested poll',
            'choices': [{'text': 'Choice A'}]
        })
        self.assertFalse(serializer.is_valid())


class ChoiceAPITest(APITestCase):

    def test_can_serialize_choice(self):
        poll = Poll.objects.create(text='Dummy poll')
        choice = Choice.objects.create(text='My choice', poll=poll, votes=10)
        serializer = ChoiceSerializer(choice)
        self.assertEqual(serializer.data, {
            'id': choice.id,
            'text': 'My choice',
            'votes': 10,
        })

    def test_votes_is_read_only(self):
        serializer = ChoiceSerializer(data={
            'text': 'Dummy Choice',
            'votes': 10
        })
        serializer.is_valid()
        poll = Poll.objects.create(text='Dummy poll')
        serializer.save(poll=poll)
        self.assertEqual(0, Choice.objects.first().votes)

    def test_can_create_choice(self):
        serializer = ChoiceSerializer(data={
            'text': 'Dummy Choice'
        })
        self.assertTrue(serializer.is_valid())

        poll = Poll.objects.create(text='Dummy poll')
        serializer.save(poll=poll)

        self.assertEqual(1, Choice.objects.count())
        choice = Choice.objects.first()
        self.assertEqual(choice.poll, poll)
        self.assertEqual(choice.text, 'Dummy Choice')
        self.assertEqual(choice.votes, 0)
