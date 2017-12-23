from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail

import time
import re

MAX_WAIT = 10
WAIT_DELAY = 0.2
TEST_EMAIL = 'mary@example.com'


class LoginTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        time.sleep(1)
        self.browser.quit()

    def wait(fn):
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(WAIT_DELAY)
        return modified_fn

    @wait
    def wait_for(self, fn):
        return fn()

    def wait_for_email_body(self):
        email = mail.outbox[0]
        if email is None:
            self.fail('Email was not found')
        return email.body

    def wait_to_be_logged_in(self, email):
        self.fail('Can not log in yet')

    def wait_to_be_logged_out(self, email):
        self.fail('Can not log out yet')

    def test_get_email_link_and_authenticate(self):
        self.browser.get(self.live_server_url)

        #  1. Mary visits the home page and types her email into the field
        email_input = self.browser.find_element_by_id('email-input')
        email_input.send_keys(TEST_EMAIL)
        email_input.send_keys(Keys.ENTER)

        #  2. The home page loads again but with a message saying
        #     to check your email
        self.wait_for(lambda: self.assertIn(
            f'Email sent to {TEST_EMAIL}',
            self.browser.find_element_by_tag_name('body').text
        ))

        #  3. Mary then finds our email
        email_body = self.wait_for_email_body()
        self.assertIn('Use this link to log in', email_body)
        url_search = re.search(r'http://.+/.+$', email_body)
        if not url_search:
            self.fail(f'could not find url in email body\n{email_body}')

        #  4. Mary then goes to the authentication link
        url = url_search.group(0)
        self.browser.get(url)

        #  5. She is authenticated now and returns to the home page
        self.wait_to_be_logged_in(TEST_EMAIL)

        #  6. She now logs out and returns back to the original page
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_to_be_logged_out(TEST_EMAIL)
