from django.test import TestCase


class HomeTest(TestCase):

    #  Test that resolve('/') is a views.HomePage
    #  Currently this doesnt work and im not sure why

    def test_home_page_using_base_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
