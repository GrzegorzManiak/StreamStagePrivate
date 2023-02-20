from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.auth_lib import (
    authenticate_key,
    check_key,
    consume_key,
    determine_key,
    generate_key,
)


class AuthLibTest(TestCase):
    def setUp(self):
        self.member = get_user_model().objects.create_user(
            username="test",
            email="test@streamstage.co",
        )

        self.key = generate_key(self.member)
        self.key2 = generate_key(self.member)

    def test_generate_key(self):
        self.assertTrue(self.key != None)
        self.assertTrue(len(self.key) > 0)
        self.assertTrue(self.key != self.key2)


    def test_check_key(self):
        self.assertTrue(check_key(self.key))

    def test_check_invalid_key(self):
        self.assertFalse(check_key("invalid_key"))


    def test_consume_key(self):
        self.assertTrue(consume_key(self.key))

    def test_consume_invalid_key(self):
        self.assertFalse(consume_key("invalid_key"))


    def test_determine_key(self):
        self.assertTrue(determine_key(self.key) == "email")

    def test_determine_invalid_key(self):
        self.assertTrue(determine_key("invalid_key") == None)


    def test_authenticate_key(self):
        self.assertTrue(authenticate_key(self.key))

    def test_authenticate_invalid_key(self):
        self.assertFalse(authenticate_key("invalid_key"))
