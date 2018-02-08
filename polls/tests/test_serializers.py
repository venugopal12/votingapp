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


class ChoiceAPITest(APITestCase):

    def test_can_serialize_choice(self):
        poll = Poll.objects.create(text='Dummy poll')
        choice = Choice.objects.create(text='My choice', poll=poll, votes=10)
        serializer = ChoiceSerializer(choice)
        self.assertEqual(serializer.data, {
            'id': choice.id,
            'text': 'My choice',
            'votes': 10
        })
