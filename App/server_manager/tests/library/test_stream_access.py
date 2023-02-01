from accounts.models import Member
from django.test import TestCase

from server_manager.models import StreamAccess
from server_manager.library import (
    generate_key, 

    get_keys_by_member_id,
    get_keys_by_stream_id,
    get_key,
    get_key_by_id,

    invalidate_key, 
    invalidate_key_by_id,
    invalidate_key_by_member_id,
)

import uuid


class StreamAccessTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create(
            username="test",
            access_level=0
        )

        self.key = StreamAccess.objects.create(
            member=self.member,
            stream="test"
        )

    
    #                                         #
    # ========= Test 'generate_key' ========= #
    #                                         #
    def test_generate_key(self):

        # -- Lets generate a key
        #    With a stream id of 1
        key = generate_key(self.member.id, 1)

        # -- Ensure the key is not None
        self.assertIsNotNone(key)

        # -- Check if the key exists
        model = StreamAccess.objects.filter(id=key.id).first()
        self.assertTrue(model != None)

        # -- Assert that the key has generated correctly
        self.assertIsNotNone(model.key)


    def test_generate_key_invalid_user(self):
        # -- Lets generate a key
        #    With a stream id of 1
        key = generate_key(uuid.uuid4(), 1)

        # -- Ensure the key is None
        self.assertIsNone(key)

    # def test_generate_key_invalid_stream(self):
    #     # -- Lets generate a key
    #     #    With a stream id of 1
    #     key = generate_key(self.member.id, uuid.uuid4())

    #     # -- Ensure the key is None
    #     self.assertIsNone(key)
    # TODO: Fix this test, Once we implement the stream model


    def test_generate_key_already_exists(self):
        # -- Lets generate a key
        key_1 = generate_key(self.member.id, 1)

        # -- Ensure the key is not None
        self.assertIsNotNone(key_1)

        # -- Check if the key exists
        self.assertTrue(StreamAccess.objects.filter(id=key_1.id).exists())

        
        # -- Lets generate a key again
        key_2 = generate_key(self.member.id, 1)

        # -- Ensure the key is not None
        self.assertIsNotNone(key_2)

        # -- Check if the key exists
        self.assertTrue(StreamAccess.objects.filter(id=key_2.id).exists())


        # -- Ensure the keys are different
        self.assertNotEqual(key_1.id, key_2.id)

        # -- Ensure that key_1 is no longer valid
        self.assertFalse(StreamAccess.objects.filter(id=key_1.id).exists())



    #                                         #
    # ====== Test invalidate_key suite ====== #
    #                                         #

    def test_invalidate_key(self):
        # -- Invalidate the key
        invalidate_key(self.key.key)

        # -- Ensure the key is no longer valid
        self.assertIsNone(get_key_by_id(self.key.id))

    def test_invalidate_key_invalid(self):
        # -- Invalidate the key
        invalidate_key(uuid.uuid4())

        # -- Ensure the key is no longer valid
        self.assertIsNotNone(get_key_by_id(self.key.id))


    def test_invalidate_key_by_id(self):
        # -- Invalidate the key
        invalidate_key_by_id(self.key.id)

        # -- Ensure the key is no longer valid
        self.assertIsNone(get_key_by_id(self.key.id))

    def test_invalidate_key_by_id_invalid(self):
        # -- Invalidate the key
        invalidate_key_by_id(uuid.uuid4())

        # -- Ensure the key is no longer valid
        self.assertIsNone(get_key_by_id(self.key.id))


    def test_invalidate_key_by_member_id(self):
        # -- Invalidate the key
        invalidate_key_by_member_id(self.member.id)

        # -- Ensure the key is no longer valid
        self.assertIsNone(get_key_by_id(self.key.id))

    def test_invalidate_key_by_member_id_invalid(self):
        # -- Invalidate the key
        invalidate_key_by_member_id(uuid.uuid4())

        # -- Ensure the key is no longer valid
        self.assertIsNone(get_key_by_id(self.key.id))
    

    #                                         #
    # ============ Test 'get_key' =========== #
    #                                         #
    def test_get_key(self):
        # -- Get the key
        key = get_key(self.key.key)

        # -- Ensure the key is not None
        self.assertIsNotNone(key)

        # -- Ensure the key is correct
        self.assertEqual(key.id, self.key.id)

    def test_get_key_invalid(self):
        # -- Get the key
        key = get_key("invalid_key")

        # -- Ensure the key is None
        self.assertIsNone(key)

    
    def test_get_key_by_id(self):
        # -- Get the key
        key = get_key_by_id(self.key.id)

        # -- Ensure the key is not None
        self.assertIsNotNone(key)

        # -- Ensure the key is correct
        self.assertEqual(key.id, self.key.id)

    def test_get_key_by_id_invalid(self):
        # -- Get the key
        key = get_key_by_id(uuid.uuid4())

        # -- Ensure the key is None
        self.assertIsNone(key)


    def test_get_key_by_member_id(self):
        # -- Get the key
        keys = get_keys_by_member_id(self.member.id)

        # -- Ensure the key is not None
        self.assertIsNotNone(keys)

        # -- Ensure the key is correct
        self.assertEqual(keys[0].id, self.key.id)

    def test_get_key_by_member_id_invalid(self):
        # -- Get the key
        keys = get_keys_by_member_id(uuid.uuid4())

        # -- Ensure the key is None
        self.assertIsNone(keys)