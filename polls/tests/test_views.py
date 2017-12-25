from django.test import TestCase
from django.contrib.auth import get_user_model
from polls.models import Poll, Choice
User = get_user_model()


class HomeTest(TestCase):

    def test_home_page_using_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_dashboard_template_when_logged_in(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'dashboard.html')


class NewPollTest(TestCase):

    def test_new_poll_uses_new_poll_template(self):
        user = User.objects.create(email='mary@example.com')
        self.client.force_login(user)
        response = self.client.get('/new')
        self.assertTemplateUsed(response, 'new_poll.html')

    def test_redirect_to_home_with_message_if_not_authenticated(self):
        response = self.client.get('/new', follow=True)
        self.assertRedirects(response, '/')
        message = list(response.context['messages'])[0]
        self.assertEqual(
            'You need to be logged in to create a poll',
            message.message
        )
        self.assertEqual(message.tags, 'error')


class ViewPollGetTest(TestCase):

    def test_poll_uses_poll_template(self):
        poll = Poll.objects.create(text='A')
        response = self.client.get(f'/poll/{poll.uid}')
        self.assertTemplateUsed(response, 'poll.html')


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
