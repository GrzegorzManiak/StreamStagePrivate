from django.contrib.auth import get_user_model
from accounts.email.verification import get_key_by_resend_key, verify_key, regenerate_key
from StreamStage.templatetags import cross_app_reverse
from django.test import TestCase
from django.test.client import RequestFactory
from StreamStage.settings import DEBUG
from django.http.response import JsonResponse

# -- Create imports
import pyotp
import json

from . import (
    username_taken,
    email_taken,
    strong_password,
    start_email_verification,
    send_reg_verification,
    temp_users
)

# -- Tests
class CreateTest(TestCase):
    def setUp(self):
        DEBUG = True
        self.user = get_user_model().objects.create_user(
            username='test',
            email='test',
            password='test',
            cased_username='test',
        )

        # -- Convert user to a dict
        self.user = self.user.__dict__
        temp_users.clear()

    # -- Functions
    def test_start_email_verification(self):
        res = start_email_verification('test1@gmail.com', 'test1', 'test1')
        self.assertTrue(res[0] != None)
        self.assertTrue(res[1] != None)
        self.assertTrue(res[2] != None)

        res = start_email_verification('test2@gmail.com', 'test2', 'test2')
        self.assertTrue(res[0] != None)
        self.assertTrue(res[1] != None)
        self.assertTrue(res[2] != None)        

    def test_username_not_taken(self):
        self.assertTrue(username_taken('test'))
        self.assertFalse(username_taken('1'))

    def test_username_taken(self):
        res = start_email_verification('1', '1', '1')
        self.assertTrue(username_taken('1'))

    def test_email_not_taken(self):
        self.assertTrue(email_taken('test'))
        self.assertFalse(email_taken('2'))

    def test_email_taken(self):
        res = start_email_verification('2', '2', '2')
        self.assertTrue(email_taken('2'))

    def test_empty_password(self):
        self.assertFalse(strong_password(''))
        
    def test_short_password(self):
        self.assertFalse(strong_password('abc123'))
        
    def test_long_password(self):
        self.assertFalse(strong_password('thispasswordistoolongtobestrongaccordingtotherequirements'))
        
    def test_password_with_spaces(self):
        self.assertFalse(strong_password('Pass word123'))
        
    def test_password_without_numbers(self):
        self.assertFalse(strong_password('Password'))
        
    def test_password_without_uppercase_letters(self):
        self.assertFalse(strong_password('password123'))
        
    def test_password_without_lowercase_letters(self):
        self.assertFalse(strong_password('PASSWORD123'))
        
    def test_strong_password(self):
        self.assertTrue(strong_password('StrongP4ssword'))


    def test_send_reg_verification_valid_details(self):
        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'send_reg_verification'
        ), { 
            'email': 'email_1@gmai.com',
            'username': 'username_1',
            'password': 'Password123!'
        })

        request.csrf_processing_done = True
        response = send_reg_verification(request)
        self.assertEqual(response.status_code, 200)

    def test_send_reg_verification_invalid_email(self):
        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'send_reg_verification'
        ), { 
            'email': 'email_1gmai.com',
            'username': 'username_14',
            'password': 'Password123!'
        })

        request.csrf_processing_done = True
        response = send_reg_verification(request)
        self.assertEqual(response.status_code, 400)

    def test_send_reg_verification_invalid_username(self):
        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'send_reg_verification'
        ), { 
            'email': 'email_2@gmail.com',
            'username': '1',
            'password': 'Password123!'
        })

        request.csrf_processing_done = True
        response = send_reg_verification(request)
        self.assertEqual(response.status_code, 400)

    def test_send_reg_verification_invalid_username(self):
        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'send_reg_verification'
        ), { 
            'email': 'email_2@gmail.com',
            'username': '1ghdsfg',
            'password': 'f!'
        })

        request.csrf_processing_done = True
        response = send_reg_verification(request)
        self.assertEqual(response.status_code, 400)

    def test_send_reg_verification(self):
        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'send_reg_verification'
        ), { 
            'email': 'email_1@gmai.com',
            'username': 'username_1',
            'password': 'Password123!'
        })

        request.csrf_processing_done = True
        response = send_reg_verification(request)
        self.assertEqual(response.status_code, 200)

        # -- Check the response
        response = json.loads(response.content)
        resend_key = response['data']['resend_token']
        key = get_key_by_resend_key(resend_key)['key']
        
        # -- Attempt to verify the key  
        res = verify_key(key)
        self.assertTrue(res[0])

        # -- Check the user was created
        user = get_user_model().objects.get(username='username_1')
        self.assertTrue(user != None)

    def test_send_reg_verification_email_change(self):
        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'send_reg_verification'
        ), { 
            'email': 'email_1@gmai.com',
            'username': 'username_1',
            'password': 'Password123!'
        })

        request.csrf_processing_done = True
        response = send_reg_verification(request)
        self.assertEqual(response.status_code, 200)

        # -- Check the response
        response = json.loads(response.content)
        resend_key = response['data']['resend_token']
        key = get_key_by_resend_key(resend_key)['key']

        # -- Attempt to resend the key
        res = regenerate_key(resend_key, 'hhhhh@gmail.com')
        self.assertTrue(res[0])

        # -- Attempt to verify the key
        res = verify_key(res[2][0])
        self.assertTrue(res[0])

        # -- Check the user was created
        user = get_user_model().objects.get(username='username_1')
        self.assertTrue(user != None)
        self.assertTrue(user.email == 'hhhhh@gmail.com')