from django.test import TestCase
from django.contrib.messages import get_messages
from unittest.mock import patch

TEST_EMAIL = 'mary@miniscruff.com'


@patch('accounts.views.send_mail')
class SendLoginEmailTests(TestCase):

    def test_redirects_to_home(self, mock_send_mail):
        response = self.client.post(
            '/account/send_login_email',
            {'email': TEST_EMAIL}
        )
        self.assertRedirects(response, '/')

    def test_should_send_email(self, mock_send_mail):
        self.client.post(
            '/account/send_login_email',
            {'email': TEST_EMAIL}
        )

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(from_email, 'noreply@vote.miniscruff.com')
        self.assertEqual(to_list, [TEST_EMAIL])

    def test_adds_success_message(self, mock_send_mail):
        response = self.client.post(
            '/account/send_login_email',
            {'email': TEST_EMAIL},
            follow=True
        )

        message = list(response.context['messages'])[0]
        self.assertEqual(
            f'Email sent to {TEST_EMAIL}',
            message.message
        )
        self.assertEqual(message.tags, 'success')
