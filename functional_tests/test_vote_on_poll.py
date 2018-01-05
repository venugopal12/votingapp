from functional_tests.base import FunctionalTest
from polls.models import Poll, Choice


class VoteOnPollTest(FunctionalTest):

    def test_vote_on_existing_poll(self):
        # create a simple poll with two choices
        poll = Poll.objects.create(text='Want a cookie?')
        choice_0 = Choice.objects.create(text='I would love one', poll=poll)
        choice_1 = Choice.objects.create(text='No thanks', poll=poll)

        # load the new poll page
        self.browser.get(self.live_server_url + f'/poll/{poll.uid}')

        # each choice has a name with the text as a slug
        self.wait_for(lambda: self.browser.find_element_by_name('choice_id'))
        choices = self.browser.find_elements_by_name('choice_label')
        self.assertEqual(len(choices), 2)
        choices[1].click()
        self.browser.find_element_by_name('vote').click()

        # now the results page should include 1 vote for I would love one
        self.wait_for(
            lambda:
                self.browser.find_element_by_name(f'{choice_0.id}-votes')
        )
        self.assertEqual(
            self.browser.find_element_by_name(f'{choice_0.id}-votes').text,
            '0 Votes'
        )
        self.assertEqual(
            self.browser.find_element_by_name(f'{choice_1.id}-votes').text,
            '1 Vote'
        )
