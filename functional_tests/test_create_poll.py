from functional_tests.base import FunctionalTest
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import (
    BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
)
User = get_user_model()


class CreatePollTest(FunctionalTest):

    def authenticate_user(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        # to set a cookie we need to first visit the domain.
        # 404 pages load the quickest!
        self.browser.get(self.live_server_url + '/404_no_page/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))

    def test_authenticated_user_creates_a_poll(self):
        question = 'Do you like python?'
        first_choice = 'First choice'
        second_choice = 'Not our first choice'

        # Mary logs in
        test_email = 'mary@example.com'
        self.authenticate_user(test_email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in()

        # She is then taken to her dashboard
        # She then clicks the new poll button
        self.wait_for(
            lambda:
                self.browser.find_element_by_name('new-poll-button').click()
        )

        # She gives it a question and two choices
        self.wait_for(
            lambda: self.browser.find_element_by_name('create-poll')
        )
        self.browser.find_element_by_name('text').send_keys(question)
        choices = self.browser.find_elements_by_name('choices')
        choices[0].send_keys(first_choice)
        choices[1].send_keys(second_choice)

        # Then she clicks create
        self.browser.find_element_by_name('create-poll').click()

        # She is then redirected to the poll page
        # Which displays her question and choices with a Vote button
        self.wait_for(
            lambda: self.browser.find_element_by_name('poll-text')
        )
        self.assertEqual(
            question,
            self.browser.find_element_by_name('poll-text').text
        )
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn(first_choice, body_text)
        self.assertIn(second_choice, body_text)
