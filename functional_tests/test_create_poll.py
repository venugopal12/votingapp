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
            lambda: self.browser.find_element_by_name('question')
        )
        self.browser.find_element_by_name('question').send_keys(question)
        self.browser.find_element_by_name('choice-1').send_keys('Yes')
        self.browser.find_element_by_name('choice-2').send_keys('No')

        # Then she clicks create
        self.browser.find_element_by_name('create-poll').click()

        print(self.browser.find_element_by_tag_name('body').text)

        # She is then redirected to the poll page
        # Which displays her question and choices with a Vote button
        self.wait_for(
            lambda: self.browser.find_element_by_name('question')
        )
        self.assertEqual(
            question,
            self.browser.find_element_by_name('question').text
        )
