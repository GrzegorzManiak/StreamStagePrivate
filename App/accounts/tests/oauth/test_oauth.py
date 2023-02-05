from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import oAuth2
from accounts.oauth.oauth import (
    check_oauth_key,
    generate_oauth_key,
    authentication_reqests,
    clean_key_store,
    format_instructions,
    OAuthTypes,

    get_oauth_data,
    remove_oauth_key
)

class OAuthTest(TestCase):
    def setUp(self):
        self.member = get_user_model().objects.create_user(
            username="test",
            email="email@streamstage.co",
        )


    def test_generate_oauth_key(self):
        # -- Generate a key
        key = generate_oauth_key(
            oauth_type=OAuthTypes.GOOGLE,
            data={}
        )

        # -- Check if the key is in the store
        self.assertTrue(key in authentication_reqests)

        # -- Check if the key is valid
        self.assertTrue(check_oauth_key(key))

    
    def test_check_oauth_key(self):
        # -- Generate a key
        key = generate_oauth_key(
            oauth_type=OAuthTypes.GOOGLE,
            data={}
        )

        # -- Check if the key is valid
        self.assertTrue(check_oauth_key(key))

        # -- Check if the key is invalid
        self.assertFalse(check_oauth_key("invalid_key"))

        
    def test_check_oauth_key_expired(self):
        # -- Generate a key
        key = generate_oauth_key(
            oauth_type=OAuthTypes.GOOGLE,
            data={},
            created=0
        )

        # -- Check if the key is valid
        self.assertFalse(check_oauth_key(key))


    def test_clean_key_store(self):
        KEYS = 10

        # -- Generate keys
        for i in range(KEYS):
            key = generate_oauth_key(
                oauth_type=OAuthTypes.GOOGLE,
                data={},
                created=0
            )

            # - Make sure the key is in the store
            self.assertTrue(key in authentication_reqests)

        # -- We should have 11 since we generated 10 keys + 1 in the setup
        self.assertTrue(len(authentication_reqests) == KEYS + 1)

        # -- Clean the store
        clean_key_store()

        # -- Check if the keys are removed
        self.assertTrue(len(authentication_reqests) == 1)


    def test_format_instructions(self):
        # -- Generate a key
        key = generate_oauth_key(
            oauth_type=OAuthTypes.GOOGLE,
            data={},
        )

        # -- Add key to oauth model
        oAuth2.objects.create(
            user=self.member,
            oauth_type=OAuthTypes.GOOGLE,
            id=key
        )

        # -- Generate instructions
        instructions = format_instructions(
            email=self.member.email,
            email_verified=True,
            oauth_type=OAuthTypes.GOOGLE,
            oauth_id=key
        )

        # -- Check if the instructions are correct
        self.assertTrue(instructions['has_account'])
        self.assertTrue(instructions['email_verified'])
        self.assertTrue(instructions['oauth_type'] == OAuthTypes.GOOGLE)
        self.assertTrue(instructions['can_authenticate'])


    def test_format_instructions_no_oauth_id(self):
        # -- Generate a key
        key = generate_oauth_key(
            oauth_type=OAuthTypes.GOOGLE,
            data={},
        )

        # -- Generate instructions
        instructions = format_instructions(
            email=self.member.email,
            email_verified=True,
            oauth_type=OAuthTypes.GOOGLE,
            oauth_id=key
        )

        # -- Check if the instructions are correct
        self.assertTrue(instructions['has_account'])
        self.assertTrue(instructions['email_verified'])
        self.assertTrue(instructions['oauth_type'] == OAuthTypes.GOOGLE)
        self.assertFalse(instructions['can_authenticate'])


    def test_format_instructions_no_oauth_type(self):
        # -- Generate a key
        key = generate_oauth_key(
            oauth_type=OAuthTypes.GOOGLE,
            data={},
        )

        # -- Add key to oauth model
        oAuth2.objects.create(
            user=self.member,
            oauth_type=OAuthTypes.GOOGLE,
            id=key
        )

        # -- Generate instructions
        instructions = format_instructions(
            email=self.member.email,
            email_verified=True,
            oauth_type=None,
            oauth_id=key
        )

        # -- Check if the instructions are correct
        self.assertTrue(instructions['has_account'])
        self.assertTrue(instructions['email_verified'])
        self.assertTrue(instructions['oauth_type'] == None)
        self.assertFalse(instructions['can_authenticate'])


    def test_format_instructions_no_oauth_id_no_oauth_type(self):
        # -- Generate a key
        key = generate_oauth_key(
            oauth_type=OAuthTypes.GOOGLE,
            data={},
        )

        # -- Generate instructions
        instructions = format_instructions(
            email=self.member.email,
            email_verified=True,
            oauth_type=None,
            oauth_id=key
        )

        # -- Check if the instructions are correct
        self.assertTrue(instructions['has_account'])
        self.assertTrue(instructions['email_verified'])
        self.assertTrue(instructions['oauth_type'] == None)
        self.assertFalse(instructions['can_authenticate'])

    

    def test_get_oauth_data(self):
        # -- Generate a key
        key = generate_oauth_key(
            oauth_type=OAuthTypes.GOOGLE,
            data={
                "email": "test"
            },
        )

        # -- Get the data
        data = get_oauth_data(key)

        # -- Check if the data is correct
        self.assertTrue(data['data']['email'] == "test")


    def test_get_oauth_data_invalid_key(self):

        # -- Get the data
        data = get_oauth_data("invalid_key")

        # -- Check if the data is correct
        self.assertTrue(data == None)
    

    def test_remove_oauth_data(self):
        # -- Generate a key
        key = generate_oauth_key(
            oauth_type=OAuthTypes.GOOGLE,
            data={
                "email": "test"
            },
        )

        # -- Get the data
        data = get_oauth_data(key)

        # -- Check if the data is correct
        self.assertTrue(data['data']['email'] == "test")

        # -- Remove the data
        remove_oauth_key(key)

        # -- Get the data
        data = get_oauth_data(key)

        # -- Check if the data is correct
        self.assertTrue(data == None)

    
    def test_remove_oauth_data_invalid_key(self):
        # -- Remove the data
        remove_oauth_key("invalid_key")

        # -- Get the data
        data = get_oauth_data("invalid_key")

        # -- Check if the data is correct
        self.assertTrue(data == None)