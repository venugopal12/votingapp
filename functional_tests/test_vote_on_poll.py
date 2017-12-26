from functional_tests.base import FunctionalTest
from polls.models import Poll, Choice


class VoteOnPollTest(FunctionalTest):

    def test_vote_on_existing_poll(self):
        # create a simple poll with two choices
        poll = Poll.objects.create(text='Want a cookie?')
        Choice.objects.create(text='I would love one', poll=poll)
        Choice.objects.create(text='No thanks', poll=poll)

        # load the new poll page
        self.browser.get(self.live_server_url + f'/poll/{poll.uid}')

        # each choice has a name with the text as a slug
        self.wait_for(lambda: self.browser.find_element_by_name('no-thanks'))
        self.browser.find_element_by_name('no-thanks').click()
        self.browser.find_element_by_name('vote').click()

        # now the results page should include 1 vote for no thanks
        self.wait_for(
            lambda:
                self.browser.find_element_by_name('no-thanks-votes')
        )
        self.assertEqual(
            self.browser.find_element_by_name('i-would-love-one-votes').text,
            '0'
        )
        self.assertEqual(
            self.browser.find_element_by_name('no-thanks').text,
            '1'
        )
