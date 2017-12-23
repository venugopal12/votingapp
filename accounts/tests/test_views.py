from django.test import TestCase
from unittest.mock import patch
from accounts.models import Token

TEST_EMAIL = 'mary@miniscruff.com'


class SendLoginEmailTests(TestCase):

    def test_redirects_to_home(self):
        response = self.client.post(
            '/account/send_login_email',
            {'email': TEST_EMAIL}
        )
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_should_send_email(self, mock_send_mail):
        self.client.post(
            '/account/send_login_email',
            {'email': TEST_EMAIL}
        )

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(from_email, 'noreply@vote.miniscruff.com')
        self.assertEqual(to_list, [TEST_EMAIL])

    def test_adds_success_message(self):
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

    @patch('accounts.views.send_mail')
    def test_sends_token_link(self, mock_send_mail):
        self.client.post(
            '/account/send_login_email',
            {'email': TEST_EMAIL}
        )

        token = Token.objects.first()
        self.assertNotEqual('', token.uid)

        expected_token_ending = f'?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_token_ending, body)
