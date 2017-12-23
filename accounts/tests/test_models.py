from unittest import TestCase
from accounts.models import Token


class TestToken(TestCase):

    def test_token_uids_unique(self):
        token1 = Token.objects.create(email='a@b.com')
        token2 = Token.objects.create(email='a@b.com')
        self.assertNotEqual(token1.uid, token2.uid)
