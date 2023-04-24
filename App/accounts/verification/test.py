from django.contrib.auth import get_user_model
from StreamStage.templatetags import cross_app_reverse
from django.test import TestCase
from django.test.client import RequestFactory
from StreamStage.settings import DEBUG
from django.http.response import JsonResponse

# -- Verification imports
from .verification import (
    temp_keys_store,
    resend_keys,
    recently_verified,

    add_key,
    get_key,
    expire_key,
    get_key_by_resend_key,
    get_resend_key_by_key,
    remove_key,
    verify_key,
    send_email,
    regenerate_key,
    check_if_verified_recently
)

# -- Tests
class VerificationTest(TestCase):
    def setUp(self):
        DEBUG = True
        self.user = get_user_model().objects.create_user(
            username='test',
            password='test',
            cased_username='test',
        )

        # -- Convert user to a dict
        self.user = self.user.__dict__
        temp_keys_store.clear()

    # -- Functions
    def test_add_key(self):
        self.assertEqual(len(temp_keys_store), 0)
        key = add_key(
            self.user,
            'test@gmail.com',
            lambda: None,
        )
        self.assertEqual(len(temp_keys_store), 1)

    def test_get_key(self):
        self.assertEqual(get_key('test'), None)
        self.assertEqual(len(temp_keys_store), 0)
        key = add_key(
            self.user,
            'test@gmail.com',
            lambda: None,
        )
        self.assertEqual(len(temp_keys_store), 1)
        new_key = get_key(key[0])
        self.assertNotEqual(new_key, None)

    def test_expire_key(self):
        self.assertEqual(get_key('test'), None)
        self.assertEqual(len(temp_keys_store), 0)
        key = add_key(
            self.user,
            'test@gmail.com',
            lambda: None,
        )
        self.assertEqual(len(temp_keys_store), 1)
        new_key = get_key(key[0])
        self.assertNotEqual(new_key, None)

        expired = expire_key(key[0])
        self.assertEqual(expired, True)
        gotten_key = get_key(key[0])
        self.assertEqual(gotten_key['created'], 0)

    def test_get_key_by_resend_key(self):
        self.assertEqual(get_key('test'), None)
        self.assertEqual(len(temp_keys_store), 0)
        key = add_key(
            self.user,
            'test@gmail.com',
            lambda: None,
        )
        self.assertEqual(len(temp_keys_store), 1)
        new_key = get_key(key[0])

        self.assertNotEqual(new_key, None)
        gotten_key = get_key_by_resend_key(key[1])
        self.assertEqual(gotten_key, new_key)
            
    def test_get_resend_key_by_key(self):
        self.assertEqual(get_key('test'), None)
        self.assertEqual(len(temp_keys_store), 0)
        key = add_key(
            self.user,
            'test@gmail.com',
            lambda: None,
        )
        self.assertEqual(len(temp_keys_store), 1)
        new_key = get_key(key[0])

        self.assertNotEqual(new_key, None)
        gotten_key = get_resend_key_by_key(key[0])
        
        self.assertEqual(gotten_key['resend_key'], key[1])

    def test_remove_key(self):
        self.assertEqual(get_key('test'), None)
        self.assertEqual(len(temp_keys_store), 0)
        key = add_key(
            self.user,
            'test@gmail.com',
            lambda: None,
        )
        self.assertEqual(len(temp_keys_store), 1)
        new_key = get_key(key[0])

        self.assertNotEqual(new_key, None)  
        removed = remove_key(key[0])
        self.assertEqual(removed[0], True)
        gotten_key = get_key(key[0])
        self.assertEqual(gotten_key, None)
        
    def test_verify_key(self):
        self.assertEqual(get_key('test'), None)
        self.assertEqual(len(temp_keys_store), 0)
        def test_callback(data):
            print('data')

        key = add_key(
            self.user,
            'test@gmail.com',
            test_callback,
        )
        self.assertEqual(len(temp_keys_store), 1)
        new_key = get_key(key[0])

        self.assertNotEqual(new_key, None)
        verified = verify_key(key[0])
        self.assertEqual(verified[0], True)
        
        # Key should be removed after verification
        gotten_key = get_key(key[0])
        self.assertEqual(gotten_key, None)

    def test_verify_expired_key(self):
        self.assertEqual(get_key('test'), None)
        self.assertEqual(len(temp_keys_store), 0)
        def test_callback(data):
            print(data)

        key = add_key(
            self.user,
            'test@gmail.com',
            test_callback,
        )
        self.assertEqual(len(temp_keys_store), 1)
        new_key = get_key(key[0])

        # -- Expire key
        expired = expire_key(key[0])
        self.assertEqual(expired, True)
        gotten_key = get_key(key[0])
        self.assertEqual(gotten_key['created'], 0)

        self.assertNotEqual(new_key, None)
        verified = verify_key(key[0])
        self.assertEqual(verified[0], False)

        # Key should be removed after verification
        gotten_key = get_key(key[0])
        self.assertEqual(gotten_key, None)
        
    def test_send_email(self):
        self.assertEqual(get_key('test'), None)
        self.assertEqual(len(temp_keys_store), 0)
        def test_callback(data):
            print(data)

        key = add_key(
            self.user,
            'test@gmail.com',
            test_callback,
        )
        self.assertEqual(len(temp_keys_store), 1)
        new_key = get_key(key[0])

        self.assertNotEqual(new_key, None)
        sent = send_email(
            key[0],
        )

        self.assertEqual(sent[0], True)

    def test_send_email_expired_key(self):
        sent = send_email('dd',)
        self.assertEqual(sent[0], False)

    def test_regenerate_key(self):
        self.assertEqual(get_key('test'), None)
        self.assertEqual(len(temp_keys_store), 0)
        def test_callback(data):
            print(data)

        key = add_key(
            self.user,
            'test@gmail.com',
            test_callback,
        )
        self.assertEqual(len(temp_keys_store), 1)
        new_key = get_key(key[0])

        self.assertNotEqual(new_key, None)
        regenerated = regenerate_key(key[1])
        self.assertEqual(regenerated[0], True)

    def test_regenerate_key_new_email(self):
        self.assertEqual(get_key('test'), None)
        self.assertEqual(len(temp_keys_store), 0)
        def test_callback(data):
            print(data)

        key = add_key(
            self.user,
            'test@gmail.com',
            test_callback,
        )
        self.assertEqual(len(temp_keys_store), 1)
        new_key = get_key(key[0])

        self.assertNotEqual(new_key, None)
        regenerated = regenerate_key(key[1], "greg@greg.greg")
        print(regenerated)
        self.assertEqual(regenerated[0], True)