from django.test import TestCase
from accounts.oauth import Google

class GoogleTest(TestCase):
    def setUp(self):
        self.google = Google()

     
    def test_url(self):
        url = self.google.url

        self.assertTrue(url != None)
        self.assertTrue(len(url) > 0)
        self.assertTrue(url.startswith("https://accounts.google.com/o/oauth2/v2/auth?"))
