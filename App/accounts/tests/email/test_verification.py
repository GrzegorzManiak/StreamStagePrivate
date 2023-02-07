from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.email.verification import (
    recently_verified,
    temp_keys_store,
    resend_keys,
    add_key,
    get_key,
    expire_key,
    remove_key,
    verify_key,
    send_email,
    regenerate_key,
    get_key_by_resend_key,
    get_resend_key_by_key,
    check_if_verified_recently,
)

class EmailVerificationTest(TestCase):
    def setUp(self):
        self.member_1 = get_user_model().objects.create_user(
            username='member_1',
            email='add@bdd.c'
        )

        self.member_2 = get_user_model().objects.create_user(
            username='member_2',
            email='add@bdd.dd'
        )

    def tearDown(self):
        temp_keys_store.clear()
        resend_keys.clear()
    
    def test_add_key(self):
        def callback():
            pass
        
        key = add_key(self.member_1, callback)

        self.assertNotEqual(key[0], key[1])
        self.assertIsNotNone(key[0])
        self.assertIsNotNone(key[1])
        self.assertEqual(len(temp_keys_store), 1)
        self.assertEqual(len(resend_keys), 1)

    def test_get_key(self):
        def callback():
            pass
        
        key = add_key(self.member_1, callback)
        key = get_key(key[0])

        self.assertIsNotNone(key)
        self.assertEqual(key['user'], self.member_1)
        self.assertEqual(key['callback'], callback)

    def test_remove_key(self):
        def callback():
            pass
        
        key = add_key(self.member_1, callback)
        

        self.assertTrue(remove_key(key[0]))
        self.assertEqual(len(temp_keys_store), 0)
        self.assertEqual(len(resend_keys), 0)

    def test_remove_key_not_found(self):
        def callback():
            pass

        key = add_key(self.member_1, callback)

        self.assertFalse(remove_key('not_found'))
        self.assertEqual(len(temp_keys_store), 1)
        self.assertEqual(len(resend_keys), 1)


    def test_verify_key(self):
        callback_called = False
        def callback(member):
            nonlocal callback_called
            callback_called = True
        
        key = add_key(self.member_1, callback)
        response = verify_key(key[0])

        self.assertTrue(response[0])
        self.assertEqual(len(temp_keys_store), 0)
        self.assertEqual(len(resend_keys), 0)
        self.assertTrue(callback_called)

    def test_verify_key_not_found(self):
        response = verify_key('not_found')

        self.assertFalse(response[0])
        self.assertEqual(len(temp_keys_store), 0)
        self.assertEqual(len(resend_keys), 0)

    def test_verify_key_expired(self):
        callback_called = False
        def callback(member):
            nonlocal callback_called
            callback_called = True
        
        key = add_key(self.member_1, callback)

        # -- Change the created time to 2 days ago
        temp_keys_store[key[0]]['created'] = 0

        response = verify_key(key[0])
        
        self.assertFalse(response[0])
        self.assertEqual(len(temp_keys_store), 0)
        self.assertEqual(len(resend_keys), 0)
        self.assertFalse(callback_called)
        

    def test_send_email(self):
        def callback():
            pass
        
        key = add_key(self.member_1, callback)
        response = send_email(key[1])
        self.assertTrue(response)

    def test_send_email_not_found(self):
        response = send_email('not_found')
        self.assertFalse(response[0])

    def test_send_email_expired(self):
        def callback():
            pass
        
        key = add_key(self.member_1, callback)

        # -- Change the created time to 2 days ago
        temp_keys_store[key[0]]['created'] = 0

        response = send_email(key[1])
        self.assertFalse(response[0])

    def test_get_key_by_resend_key(self):
        def callback():
            pass
        
        key = add_key(self.member_1, callback)
        response = get_key_by_resend_key(key[1])

        self.assertIsNotNone(response)
        self.assertEqual(response['user'], self.member_1)
        self.assertEqual(response['callback'], callback)

    def test_regenerate_key(self):
        def callback():
            pass
        
        key = add_key(self.member_1, callback)
        response = regenerate_key(key[1])
        self.assertTrue(response)

    def test_regenerate_key_not_found(self):
        response = regenerate_key('not_found')
        self.assertIsNone(response)

    def test_regenerate_key_expired(self):
        def callback():
            pass
        
        key = add_key(self.member_1, callback)

        # -- Change the created time to 2 days ago
        temp_keys_store[key[0]]['created'] = 0

        response = regenerate_key(key[1])
        self.assertIsNone(response)

    
    def test_get_resend_key_by_key(self):
        def callback():
            pass
        
        key = add_key(self.member_1, callback)
        response = get_resend_key_by_key(key[0])

        self.assertEqual(response['resend_key'], key[1])

    def test_get_resend_key_by_key_not_found(self):
        response = get_resend_key_by_key('not_found')
        self.assertIsNone(response)

    
    def test_check_if_verified_recently(self):
        def callback(user):
            pass
        
        key = add_key(self.member_1, callback)
        response = check_if_verified_recently(key[2])
        self.assertFalse(response)

        verify_key(key[0])
        response = check_if_verified_recently(key[2])
        self.assertTrue(response)

    def test_check_if_verified_recently_not_found(self):
        response = check_if_verified_recently('not_found')
        self.assertFalse(response)

    def test_check_if_verified_recently_expired(self):
        def callback(user):
            pass
        
        key = add_key(self.member_1, callback)

        # -- Change the created time to 2 days ago
        temp_keys_store[key[0]]['created'] = 0

        response = check_if_verified_recently(key[2])
        self.assertFalse(response)

        verify_key(key[0])
        response = check_if_verified_recently(key[2])
        self.assertFalse(response)


    def test_expire_key(self):
        def callback():
            pass
        
        key = add_key(self.member_1, callback)
        expire_key(key[0])

        self.assertFalse(verify_key(key[0])[0])

    