from django.contrib.auth import get_user_model
from StreamStage.templatetags import cross_app_reverse
from django.test import TestCase
from django.test.client import RequestFactory
from StreamStage.settings import DEBUG

# -- MFA imports
import pyotp
import json
from . import (
    check_duplicate,
    delete_duplicate,
    generate_token,
    has_token,
    get_token,
    verify_temp_otp,

    setup_mfa,
    verify_mfa,
    disable_mfa,
)

from accounts.profile import generate_pat

# -- Tests
class MFATest(TestCase):
    def setUp(self):
        DEBUG = True
        self.user = get_user_model().objects.create_user(
            username='test',
            password='test',
            cased_username='test',
        )

        # -- Convert user to a dict
        self.user = self.user.__dict__

    # -- Functions
    def test_has_token(self):
        self.assertFalse(has_token({}))
        self.assertFalse(has_token(self.user))
        generate_token(self.user)
        self.assertTrue(has_token(self.user))

    def test_get_token(self):
        self.assertEqual(get_token({})[0], None)
        self.assertEqual(get_token(self.user)[0], None)
        token = generate_token(self.user)
        self.assertEqual(get_token(self.user)[0], token)

    def test_check_duplicate(self):
        self.assertFalse(check_duplicate(self.user))
        generate_token(self.user)
        self.assertTrue(check_duplicate(self.user))
        delete_duplicate(self.user)
        self.assertFalse(check_duplicate(self.user))

    def test_delete_duplicate(self):
        generate_token(self.user)
        self.assertTrue(check_duplicate(self.user))
        delete_duplicate(self.user)
        self.assertFalse(check_duplicate(self.user))

    def test_verify_temp_otp(self):
        token = generate_token(self.user)
        self.assertFalse(get_token(self.user)[0] == True)
        totp = pyotp.TOTP(token)
        self.assertTrue(verify_temp_otp(self.user, totp.now()))

        delete_duplicate(self.user)
        self.assertEqual(verify_temp_otp(self.user, totp.now())[0], False)
        self.assertFalse(get_token(self.user)[0] == True)


    # -- Views
    def test_setup_mfa_invalid(self):
        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'setup_mfa'
        ), { 'token': '' })

        # -- Test the view
        request.user = get_user_model().objects.get(pk=self.user['id'])
        request.csrf_processing_done = True
        response = setup_mfa(request)

        self.assertEqual(response.status_code, 400)

    def test_setup_mfa_valid(self):
        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'setup_mfa'
        ), { 'token': generate_pat(self.user) })

        # -- Test the view
        request.user = get_user_model().objects.get(pk=self.user['id'])
        request.csrf_processing_done = True
        response = setup_mfa(request)

        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        token = json_data['data']['token']

        self.assertEqual(token, get_token(self.user)[0])

    
    def test_verify_mfa_invalid(self):
        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'verify_mfa'
        ), { 
            'token': '',
            'otp': ''
        })

        # -- Test the view
        request.user = get_user_model().objects.get(pk=self.user['id'])
        request.csrf_processing_done = True
        response = verify_mfa(request)

        self.assertEqual(response.status_code, 400)


    def test_verify_mfa_valid(self):
        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'verify_mfa'
        ), { 
            'token': generate_pat(self.user),
            'otp': pyotp.TOTP(generate_token(self.user)).now()
        })

        # -- Test the view
        request.user = get_user_model().objects.get(pk=self.user['id'])
        request.csrf_processing_done = True
        response = verify_mfa(request)

        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        
        self.assertEqual(json_data['status'], 'success')
        self.assertEqual(response.status_code, 200)


    def test_disable_mfa_invalid(self):
        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'disable_mfa'
        ), { 'token': '' })

        # -- Test the view
        request.user = get_user_model().objects.get(pk=self.user['id'])
        request.csrf_processing_done = True
        response = disable_mfa(request)

        self.assertEqual(response.status_code, 400)


    def test_disable_mfa_valid(self):
        # -- Setup the request
        request = RequestFactory()
        request = request.post(cross_app_reverse(
            'accounts', 'disable_mfa'
        ), { 'token': generate_pat(self.user) })

        # -- Test the view
        request.user = get_user_model().objects.get(pk=self.user['id'])
        request.csrf_processing_done = True
        response = disable_mfa(request)

        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        
        self.assertEqual(json_data['status'], 'success')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(has_token(self.user))