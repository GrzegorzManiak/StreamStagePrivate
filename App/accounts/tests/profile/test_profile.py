from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.profile.profile import (
    validate_username,
    change_description,
    change_username
)

class TestProfile(TestCase):
    def setUp(self):
        self.user_1 = get_user_model().objects.create_user(
            username='test',
            email='Some@dude.com'
        )

        self.user_2 = get_user_model().objects.create_user(
            username='test2',
            email='Some@dude2.com'
        )

    
    """
        -- Must be between 3 and 20 characters
        -- Must Start with a letter
        -- Must only contain letters, numbers, and underscores
        -- Must not contain two underscores in a row
        -- Must not end with an underscore
    """
    def test_validate_username(self):
        valid_usernames = [
            'test',
            'test23',
            'test_23',
            'test_2_3',
        ]

        invalid_usernames = [
            'te',
            'test_',
            'test__',
            'test__23',
            'test_23_',
            'test_2__3',
            'ImAReallyLongUsernameThatIsWayTooLong',
            'Ive got spaces',
        ]

        for username in valid_usernames:
            self.assertEqual(validate_username(username)[0], True)

        for username in invalid_usernames:
            self.assertEqual(validate_username(username)[0], False)


    def test_change_username(self):
        
        res = change_username(self.user_1, 'Test5')
        self.assertEqual(res[0], True)
        self.assertEqual(self.user_1.username, 'test5')

    def test_change_username_same(self):
        res = change_username(self.user_1, 'test')
        self.assertEqual(res[0], False)
        self.assertEqual(self.user_1.username, 'test')

    def test_change_username_taken(self):
        res = change_username(self.user_1, 'test2')
        self.assertEqual(res[0], False)
        self.assertEqual(self.user_1.username, 'test')


    def test_change_description(self):
        res = change_description(self.user_1, 'This is a test description')
        self.assertEqual(res[0], True)
        self.assertEqual(self.user_1.description, 'This is a test description')

    def test_change_description_same(self):
        res = change_description(self.user_1, self.user_1.description)
        self.assertEqual(res[0], False)
        self.assertEqual(self.user_1.description, '')