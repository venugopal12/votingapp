from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

User = get_user_model()


class PasswordLessAuthenticationTest(TestCase):

    def test_returns_None_if_no_such_token(self):
        result = PasswordlessAuthenticationBackend().authenticate(
            'no-such-token'
        )
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        email = 'mary@example.com'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        email = 'mary@example.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        new_user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(existing_user, new_user)

    def test_gets_user_by_email(self):
        desired_email = 'mary@example.com'
        desired_user = User.objects.create(email=desired_email)
        found_user = PasswordlessAuthenticationBackend().get_user(
            desired_email
        )
        self.assertEqual(desired_user, found_user)

    def test_returns_None_if_no_user_with_that_email(self):
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user('a@b.com')
        )

    def test_authenticate_removes_token_if_valid(self):
        email = 'mary@example.com'
        User.objects.create(email=email)
        token = Token.objects.create(email=email)
        PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(Token.objects.count(), 0)
