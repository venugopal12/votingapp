from django.test import TestCase
from django.contrib.auth import get_user_model
from polls.models import Poll
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
        response = self.client.get('/new')
        self.assertTemplateUsed(response, 'new_poll.html')


class ViewPollTest(TestCase):

    def test_view_poll_uses_view_poll_template(self):
        poll = Poll.objects.create(question_text='A')
        response = self.client.get(f'/poll/{poll.uid}')
        self.assertTemplateUsed(response, 'poll.html')
