from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium import webdriver

import time

MAX_WAIT = 10
WAIT_DELAY = 0.2


class FunctionalTest(StaticLiveServerTestCase):

    def wait(fn):
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e  # noqa
                    time.sleep(WAIT_DELAY)
        return modified_fn

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def wait_to_be_logged_in(self):
        self.browser.find_element_by_name('logout-button')

    @wait
    def wait_to_be_logged_out(self):
        self.browser.find_element_by_name('email')

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
