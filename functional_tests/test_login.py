from selenium.webdriver.common.keys import Keys
from django.core import mail
from functional_tests.base import FunctionalTest

import re


class LoginTest(FunctionalTest):

    def wait_for_email_body(self):
        email = mail.outbox[0]
        return email.body

    def test_get_email_link_and_authenticate(self):
        test_email = 'mary@example.com'

        self.browser.get(self.live_server_url)

        #  1. Mary visits the home page and types her email into the field
        email_input = self.browser.find_element_by_name('email')
        email_input.send_keys(test_email)
        email_input.send_keys(Keys.ENTER)

        #  2. The home page loads again but with a message saying
        #     to check your email
        self.wait_for(lambda: self.assertIn(
            f'Email sent to {test_email}',
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
        self.wait_to_be_logged_in()

        #  6. She now logs out and returns back to the original page
        self.browser.find_element_by_name('logout-button').click()
        self.wait_to_be_logged_out()
