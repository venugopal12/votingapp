from django.test import TestCase
from unittest.mock import patch, call
from accounts.models import Token, User

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

        expected_token_ending = f'/login?uid={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_token_ending, body)


@patch('accounts.views.auth')
class LoginTests(TestCase):

    def test_redirects_to_home(self, mock_auth):
        response = self.client.get('/account/login?uid=abcd1234')
        self.assertRedirects(response, '/')

    def test_does_not_call_login_if_invalid_token(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get('/account/login?uid=abcd1234')
        self.assertFalse(mock_auth.login.called)

    def test_authenticates_with_uid(self, mock_auth):
        self.client.get('/account/login?uid=abcd1234')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abcd1234')
        )

    def test_login_with_valid_token(self, mock_auth):
        response = self.client.get('/account/login?uid=abcd1234')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_displays_welcome_message_on_success(self, mock_auth):
        email = 'mary@example.com'
        user = User(email=email)
        mock_auth.authenticate.return_value = user
        token = Token.objects.create(email=email)
        response = self.client.get(
            f'/account/login?uid={token.uid}',
            follow=True
        )
        message = list(response.context['messages'])[0]
        self.assertEqual(
            'Welcome mary!',
            message.message
        )
        self.assertEqual(message.tags, 'success')

    def test_displays_error_on_failure(self, mock_auth):
        mock_auth.authenticate.return_value = None
        response = self.client.get('/account/login?uid=abcd1234', follow=True)
        message = list(response.context['messages'])[0]
        self.assertEqual(
            'Unable to authenticate, please try again',
            message.message
        )
        self.assertEqual(message.tags, 'error')
