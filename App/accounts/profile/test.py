from django.contrib.auth import get_user_model
from accounts.models import Member
from StreamStage.templatetags import cross_app_reverse
from django.test import TestCase
from django.test.client import RequestFactory
from StreamStage.settings import DEBUG

# -- MFA imports
import json
import datetime
import time
from . import (
    validate_username,
    change_username,
    change_description,
    update_profile,
    generate_pat,
    get_pat,
    temporary_pats,
    validate_pat,
    extend_pat,
    revoke_pat,
)

# -- Tests
class ProfileTest(TestCase):
    def setUp(self):
        DEBUG = True
        self.user = get_user_model().objects.create_user(
            username='test',
            password='test',
            cased_username='test',
        )

        # -- Convert user to a dict
        self.user.ensure()
        self.user = self.user.__dict__

    # -- Functions
    def test_validate_username(self):
        self.assertFalse(validate_username('')[0])
        self.assertFalse(validate_username('a')[0])
        self.assertFalse(validate_username('a'*33)[0])
        self.assertFalse(validate_username('1name')[0])
        self.assertFalse(validate_username('na__me')[0])
        self.assertFalse(validate_username('name_')[0])
        self.assertFalse(validate_username('na me')[0])
        self.assertTrue(validate_username('na-me')[0])

    def test_change_username(self):
        self.assertFalse(change_username(self.user, '')[0])
        self.user = get_user_model().objects.get(id=self.user['id']).__dict__
        self.assertNotEqual(self.user['username'], '')

        self.assertFalse(change_username(self.user, 'a')[0])
        self.user = get_user_model().objects.get(id=self.user['id']).__dict__
        self.assertNotEqual(self.user['username'], 'a')

        self.assertFalse(change_username(self.user, 'a'*33)[0])
        self.user = get_user_model().objects.get(id=self.user['id']).__dict__
        self.assertNotEqual(self.user['username'], 'a'*33)

        self.assertFalse(change_username(self.user, '1name')[0])
        self.user = get_user_model().objects.get(id=self.user['id']).__dict__
        self.assertNotEqual(self.user['username'], '1name')

        self.assertFalse(change_username(self.user, 'na__me')[0])
        self.user = get_user_model().objects.get(id=self.user['id']).__dict__
        self.assertNotEqual(self.user['username'], 'na__me')

        self.assertFalse(change_username(self.user, 'name_')[0])
        self.user = get_user_model().objects.get(id=self.user['id']).__dict__
        self.assertNotEqual(self.user['username'], 'name_')

        self.assertFalse(change_username(self.user, 'na me')[0])
        self.user = get_user_model().objects.get(id=self.user['id']).__dict__
        self.assertNotEqual(self.user['username'], 'na me')

        self.assertTrue(change_username(self.user, 'na-me')[0])
        self.user = get_user_model().objects.get(id=self.user['id']).__dict__
        self.assertEqual(self.user['username'], 'na-me')

        self.assertTrue(change_username(self.user, 'true')[0])
        self.user = get_user_model().objects.get(id=self.user['id']).__dict__
        self.assertEqual(self.user['username'], 'true')

    def test_change_description(self):
        # 300 max, or the same
        self.assertTrue(change_description(self.user, '')[0])
        self.user = get_user_model().objects.get(id=self.user['id']).__dict__
        self.assertEqual(self.user['description'], '')

        self.assertFalse(change_description(self.user, 'a'*301)[0])
        self.user = get_user_model().objects.get(id=self.user['id']).__dict__
        self.assertEqual(self.user['description'], '')

        self.assertTrue(change_description(self.user, 'a'*300)[0])
        self.user = get_user_model().objects.get(id=self.user['id']).__dict__
        self.assertEqual(self.user['description'], 'a'*300)
    
    def test_update_profile(self):
        data = {'first_name': 'Test', 'last_name': 'User', 'description': 'This is a test user'}
        result = update_profile(self.user, data)
        self.assertTrue(result[0])

        data = {}
        result = update_profile(self.user, data)
        self.assertFalse(result[0])

        data = {'first_name': 'Test', 'last_name': 'User', 'description': 'This is a test user'}
        result = update_profile(self.user, data)
        self.assertTrue(result[0])

        data = 'not a dictionary'
        result = update_profile(self.user, data)
        self.assertFalse(result[0])

        data = {'email': 'new_test@example.com'}
        result = update_profile(self.user, data)
        self.assertFalse(result[0])

        user1 = Member.objects.create(username='test_user1', password='test_password1', email='test1@example.com')
        user1.ensure()
        user2 = Member.objects.create(username='test_user2', password='test_password2', email='test2@example.com')
        user2.ensure()
        data = {'username': 'test_user2'}
        result = update_profile(user1, data)
        self.assertFalse(result[0])

        data = { 'password': 'test_password1' }
        result = update_profile(self.user, data)
        self.assertFalse(result[0])

        data = {'old_password': 'wrong_password', 'password': 'new_password'}
        result = update_profile(self.user, data, True)
        self.assertFalse(result[0])

        data = {'old_password': 'test', 'password': 'new_password'}
        result = update_profile(self.user, data, True)
        self.assertTrue(result[0])

    def test_generate_pat(self):
        result = generate_pat(self.user)
        self.assertNotEqual(result, '')

        token = get_pat(result)
        self.assertEqual(token[0]['token'], result)

    def test_get_pat(self):
        result = generate_pat(self.user)
        self.assertNotEqual(result, '')

        token = get_pat(result)
        self.assertEqual(token[0]['token'], result)

        for pat in temporary_pats:
            pat['time'] = time.time() - (60 * 20) # 20 minutes ago
                
        token = get_pat(result)
        self.assertEqual(token[0], None)

        token = get_pat('not a token')
        self.assertEqual(token[0], None)

    def test_validate_pat(self):
        result = generate_pat(self.user)
        self.assertNotEqual(result, '')

        token = get_pat(result)
        self.assertEqual(token[0]['token'], result)

        self.assertTrue(validate_pat(result, self.user)[0])
        self.assertFalse(validate_pat('not a token', self.user)[0])

        for pat in temporary_pats:
            pat['time'] = time.time() - (60 * 20)

        self.assertFalse(validate_pat(result, self.user)[0])

    def test_extend_pat(self):
        result = generate_pat(self.user)
        self.assertNotEqual(result, '')

        token = get_pat(result)
        self.assertEqual(token[0]['token'], result)

        self.assertTrue(validate_pat(result, self.user)[0])
        
        temporary_pats[0]['time'] = temporary_pats[0]['time'] - (60 * 10)
        time_left = temporary_pats[0]['time'] - time.time()
        self.assertTrue(time_left < 60 * 15)
        time_left = temporary_pats[0]['time']

        self.assertTrue(extend_pat(result, self.user)[0])
        self.assertTrue(time_left > 60 * 10)
        self.assertTrue(validate_pat(result, self.user)[0])

    def test_revoke_pat(self):
        result = generate_pat(self.user)
        self.assertNotEqual(result, '')

        token = get_pat(result)
        self.assertEqual(token[0]['token'], result)

        self.assertTrue(validate_pat(result, self.user)[0])
        self.assertTrue(revoke_pat(result, self.user)[0])
        self.assertFalse(validate_pat(result, self.user)[0])
