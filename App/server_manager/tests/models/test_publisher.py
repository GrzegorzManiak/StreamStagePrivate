from accounts.models import Member
from django.test import TestCase

from server_manager.models import Publisher

class PublisherTest(TestCase):

    def setUp(self):
        self.member_1 = Member.objects.create(username="user_1", access_level=0)
        self.member_2 = Member.objects.create(username="user_2", access_level=0)
        self.member_3 = Member.objects.create(username="user_3", access_level=0)

        self.publisher = Publisher.objects.create(
            name="test",
            description="test",
        )

    #                                          #
    # ============= Member Tests ============= #
    #                                          #
    
    def test_add_member(self):
        # -- Lets add a member to the publisher
        self.publisher.add_member(self.member_1)

        # -- Ensure the member is in the list
        self.assertTrue(self.member_1 in self.publisher.members.all())

    def test_add_invalid_member(self):
        # -- Lets add a member to the publisher
        self.publisher.add_member(self.member_1)

        # -- Ensure the member is in the list
        self.assertFalse(self.member_2 in self.publisher.members.all())

    def test_add_same_member_twice(self):
        # -- Lets add a member to the publisher
        self.publisher.add_member(self.member_1)

        # -- Lets add the same member to the publisher
        self.publisher.add_member(self.member_1)

        # -- Ensure the member is in the list only once
        self.assertEqual(self.publisher.members.count(), 1)

    def test_add_multiple_members(self):
        # -- Lets add a member to the publisher
        self.publisher.add_member(self.member_1)
        self.publisher.add_member(self.member_2)
        self.publisher.add_member(self.member_3)

        # -- Ensure the members are in the list
        self.assertTrue(self.member_1 in self.publisher.members.all())
        self.assertTrue(self.member_2 in self.publisher.members.all())
        self.assertTrue(self.member_3 in self.publisher.members.all())


    def test_remove_member(self):
        # -- Lets add a member to the publisher
        self.publisher.add_member(self.member_1)

        # -- Lets remove the member from the publisher
        self.publisher.remove_member(self.member_1)

        # -- Ensure the member is not in the list
        self.assertFalse(self.member_1 in self.publisher.members.all())

    def test_remove_invalid_member(self):
        # -- Lets add a member to the publisher
        self.publisher.add_member(self.member_1)

        # -- Lets remove the member from the publisher
        self.publisher.remove_member(self.member_2)

        # -- Ensure the member is still in the list
        self.assertTrue(self.member_1 in self.publisher.members.all())

    def test_remove_same_member_twice(self):
        # -- Lets add a member to the publisher
        self.publisher.add_member(self.member_1)

        # -- Lets remove the member from the publisher
        self.publisher.remove_member(self.member_1)

        # -- Lets remove the member from the publisher
        self.publisher.remove_member(self.member_1)

        # -- Ensure the member is not in the list
        self.assertFalse(self.member_1 in self.publisher.members.all())

    
    def test_is_member(self):
        # -- Lets add a member to the publisher
        self.publisher.add_member(self.member_1)

        # -- Lets check if the member is in the publisher
        self.assertTrue(self.publisher.is_member(self.member_1))

    def test_is_invalid_member(self):
        # -- Lets add a member to the publisher
        self.publisher.add_member(self.member_1)

        # -- Lets check if the member is in the publisher
        self.assertFalse(self.publisher.is_member(self.member_2))


    def test_get_members(self):
        # -- Lets add a member to the publisher
        self.publisher.add_member(self.member_1)

        # -- Lets check if the member is in the publisher
        self.assertTrue(self.member_1 in self.publisher.get_members())

    def test_get_invalid_member(self):
        # -- Lets add a member to the publisher
        self.publisher.add_member(self.member_1)

        # -- Lets check if the member is in the publisher
        self.assertFalse(self.member_2 in self.publisher.get_members())

    def test_get_multiple_members(self):
        # -- Lets add a member to the publisher
        self.publisher.add_member(self.member_1)
        self.publisher.add_member(self.member_2)
        self.publisher.add_member(self.member_3)

        # -- Lets check if the member is in the publisher
        self.assertTrue(self.member_1 in self.publisher.get_members())
        self.assertTrue(self.member_2 in self.publisher.get_members())
        self.assertTrue(self.member_3 in self.publisher.get_members())


    #                                          #
    # ============= Server Tests ============= #
    #                                          #
    
    # TODO: Add tests for servers here once 
    #       the server model is implemented