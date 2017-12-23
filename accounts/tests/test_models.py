from django.test import TestCase
from accounts.models import Token
from django.contrib.auth import get_user_model, login

User = get_user_model()


class UserModelTest(TestCase):

    def test_is_valid_with_only_email(self):
        user = User(email='a@b.com')
        user.full_clean()  # should not raise

    def test_email_is_primary_key(self):
        user = User(email='a@b.com')
        self.assertEqual(user.pk, 'a@b.com')

    def test_no_problem_with_auth_login(self):
        user = User.objects.create(email='a@b.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        login(request, user)  # should not raise


class TokenModelTest(TestCase):

    def test_token_uids_unique(self):
        token1 = Token.objects.create(email='a@b.com')
        token2 = Token.objects.create(email='a@b.com')
        self.assertNotEqual(token1.uid, token2.uid)
