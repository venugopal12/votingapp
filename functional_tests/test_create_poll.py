from functional_tests.base import FunctionalTest


class CreatePollTest(FunctionalTest):

    def test_authenticated_user_creates_a_poll(self):
        question = 'Do you like python?'
        first_choice = 'First choice'
        second_choice = 'Not our first choice'

        self.browser.get(self.live_server_url)

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
