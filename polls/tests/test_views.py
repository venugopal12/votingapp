from django.test import TestCase
from polls.models import Poll, Choice


class HomeTest(TestCase):

    def test_home_page_using_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class NewPollTest(TestCase):

    def test_new_poll_uses_new_poll_template(self):
        response = self.client.get('/new')
        self.assertTemplateUsed(response, 'new_poll.html')


class ViewPollGetTest(TestCase):

    def test_uses_poll_template(self):
        poll = Poll.objects.create(text='A')
        response = self.client.get(f'/poll/{poll.uid}')
        self.assertTemplateUsed(response, 'poll.html')

    def test_displays_text_and_choices(self):
        text = 'Would you like a cookie?'
        choice_0 = 'Yes of course'
        choice_1 = 'Not really, I am full'
        poll = Poll.objects.create(text=text)
        Choice.objects.create(text=choice_0, poll=poll)
        Choice.objects.create(text=choice_1, poll=poll)
        response = self.client.get(f'/poll/{poll.uid}')
        self.assertContains(response, text)
        self.assertContains(response, choice_0)
        self.assertContains(response, choice_1)

    def test_choices_have_css_name_of_choice_id(self):
        # create another poll and some choices, so our real poll isnt the first
        random_poll = Poll.objects.create(text='Random poll')
        for _ in range(5):
            Choice.objects.create(text='random choice', poll=random_poll)

        poll = Poll.objects.create(text='Would you like a cookie?')
        choice_0 = Choice.objects.create(text='Yes of course', poll=poll)
        choice_1 = Choice.objects.create(text='Not really', poll=poll)
        response = self.client.get(f'/poll/{poll.uid}')
        self.assertContains(
            response,
            f'name="choice_id" value="{choice_0.id}"'
        )
        self.assertContains(
            response,
            f'name="choice_id" value="{choice_1.id}"'
        )

    def test_contains_hidden_field_for_poll_uid(self):
        poll = Poll.objects.create(text='Would you like a cookie?')
        Choice.objects.create(text='Yes of course', poll=poll)
        Choice.objects.create(text='Not really', poll=poll)
        response = self.client.get(f'/poll/{poll.uid}')
        self.assertContains(response, f'name="poll_uid" value="{poll.uid}"')

    def test_passes_in_correct_poll(self):
        Poll.objects.create(text='some other poll')
        poll = Poll.objects.create(text='my new poll')
        response = self.client.get(f'/poll/{poll.uid}')
        self.assertEqual(response.context['poll'], poll)


class ViewPollPostTest(TestCase):

    def test_creates_poll(self):
        self.client.post('/poll', {
            'text': 'Poll Text',
            'choices': ['A', 'B']
        })

        new_poll = Poll.objects.first()
        self.assertEqual('Poll Text', new_poll.text)

        choices = list(Choice.objects.filter(poll=new_poll))
        self.assertEqual(len(choices), 2)
        self.assertEqual(choices[0].text, 'A')
        self.assertEqual(choices[1].text, 'B')

    def test_redirects_to_new_poll(self):
        response = self.client.post('/poll', {
            'text': 'Poll Text',
            'choices': ['A', 'B']
        })
        new_poll = Poll.objects.first()
        self.assertRedirects(response, f'/poll/{new_poll.uid}')


class ResultsTest(TestCase):

    def test_uses_results_template(self):
        poll = Poll.objects.create(text='A')
        response = self.client.get(f'/poll/{poll.uid}/results')
        self.assertTemplateUsed(response, 'results.html')

    def test_passes_in_correct_poll(self):
        Poll.objects.create(text='some other poll')
        poll = Poll.objects.create(text='The question we are asking')
        response = self.client.get(f'/poll/{poll.uid}/results')
        self.assertEqual(response.context['poll'], poll)


class VoteTest(TestCase):

    def test_redirects_to_results_page(self):
        poll = Poll.objects.create(text='A')
        choice = Choice.objects.create(text='123', poll=poll)
        response = self.client.post(f'/vote', data={
            'poll_uid': poll.uid,
            'choice_id': choice.id
        })
        self.assertRedirects(response, f'/poll/{poll.uid}/results')

    def test_increases_vote_by_one(self):
        poll = Poll.objects.create(text='A')
        choice = Choice.objects.create(text='123', poll=poll)
        self.client.post(f'/vote', data={
            'poll_uid': poll.uid,
            'choice_id': choice.id
        })
        # we have to get the new choice from the database
        # the existing one we have above wont be updated
        self.assertEqual(Choice.objects.get(id=choice.id).votes, 1)

    def test_can_vote_more_than_once(self):
        poll = Poll.objects.create(text='A')
        choice = Choice.objects.create(text='123', poll=poll)
        self.client.post(f'/vote', data={
            'poll_uid': poll.uid,
            'choice_id': choice.id
        })
        self.client.post(f'/vote', data={
            'poll_uid': poll.uid,
            'choice_id': choice.id
        })
        self.assertEqual(Choice.objects.get(id=choice.id).votes, 2)
