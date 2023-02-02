from accounts.models import Member
from django.test import TestCase
from server_manager.library import ServerMode

from server_manager.models.publisher import Publisher
from server_manager.models.server import Server

class PublisherTest(TestCase):

    def setUp(self):
        self.member_1 = Member.objects.create(username="user_1", access_level=0, email="1@2.com")
        self.member_2 = Member.objects.create(username="user_2", access_level=0, email="2@3.com")
        self.member_3 = Member.objects.create(username="user_3", access_level=0, email="3@4.com")

        self.server_1 = Server.objects.create(slug="server_1", name="server_1")
        self.server_2 = Server.objects.create(slug="server_2", name="server_2")
        self.server_3 = Server.objects.create(slug="server_3", name="server_3")

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
    
    def test_add_server(self):
        # -- Lets add a server to the publisher
        self.publisher.add_server(self.server_1)

        # -- Ensure the server is in the list
        self.assertTrue(self.server_1 in self.publisher.server_list.all())

    def test_add_invalid_server(self):
        # -- Lets add a server to the publisher
        self.publisher.add_server(self.server_1)

        # -- Ensure the server is in the list
        self.assertFalse(self.server_2 in self.publisher.server_list.all())

    def test_add_same_server_twice(self):
        # -- Lets add a server to the publisher
        self.publisher.add_server(self.server_1)

        # -- Lets add the same server to the publisher
        self.publisher.add_server(self.server_1)

        # -- Ensure the server is in the list only once
        self.assertEqual(self.publisher.server_list.count(), 1)

    def test_add_multiple_servers(self):
        # -- Lets add a server to the publisher
        self.publisher.add_server(self.server_1)
        self.publisher.add_server(self.server_2)
        self.publisher.add_server(self.server_3)

        # -- Ensure the servers are in the list
        self.assertTrue(self.server_1 in self.publisher.server_list.all())
        self.assertTrue(self.server_2 in self.publisher.server_list.all())
        self.assertTrue(self.server_3 in self.publisher.server_list.all())

    
    def test_remove_server(self):
        # -- Lets add a server to the publisher
        self.publisher.add_server(self.server_1)

        # -- Lets remove the server from the publisher
        self.publisher.remove_server(self.server_1)

        # -- Ensure the server is not in the list
        self.assertFalse(self.server_1 in self.publisher.server_list.all())

    def test_remove_invalid_server(self):
        # -- Lets add a server to the publisher
        self.publisher.add_server(self.server_1)

        # -- Lets remove the server from the publisher
        self.publisher.remove_server(self.server_2)

        # -- Ensure the server is still in the list
        self.assertTrue(self.server_1 in self.publisher.server_list.all())

    def test_remove_same_server_twice(self):
        # -- Lets add a server to the publisher
        self.publisher.add_server(self.server_1)

        # -- Lets remove the server from the publisher
        self.publisher.remove_server(self.server_1)

        # -- Lets remove the server from the publisher
        self.publisher.remove_server(self.server_1)

        # -- Ensure the server is not in the list
        self.assertFalse(self.server_1 in self.publisher.server_list.all())

    
    def test_has_server(self):
        # -- Lets add a server to the publisher
        self.publisher.add_server(self.server_1)

        # -- Lets check if the server is in the publisher
        self.assertTrue(self.publisher.has_server(self.server_1))

    def test_has_invalid_server(self):
        # -- Lets add a server to the publisher
        self.publisher.add_server(self.server_1)

        # -- Lets check if the server is in the publisher
        self.assertFalse(self.publisher.has_server(self.server_2))

    
    def test_get_servers(self):
        # -- Lets add a server to the publisher
        self.publisher.add_server(self.server_1)

        # -- Lets check if the server is in the publisher
        self.assertTrue(self.server_1 in self.publisher.get_servers())

    def test_get_invalid_server(self):
        # -- Lets add a server to the publisher
        self.publisher.add_server(self.server_1)

        # -- Lets check if the server is in the publisher
        self.assertFalse(self.server_2 in self.publisher.get_servers())

    def test_get_multiple_servers(self):
        # -- Lets add a server to the publisher
        self.publisher.add_server(self.server_1)
        self.publisher.add_server(self.server_2)
        self.publisher.add_server(self.server_3)

        # -- Lets check if the server is in the publisher
        self.assertTrue(self.server_1 in self.publisher.get_servers())
        self.assertTrue(self.server_2 in self.publisher.get_servers())
        self.assertTrue(self.server_3 in self.publisher.get_servers())


    #                                          #
    # ============= ingest Tests ============= #
    #                                          #
    def test_set_ingest_server(self):
        # -- Make sure server 1 is an ingest server
        self.server_2.set_mode(ServerMode.INGEST)

        # -- Lets set the ingest server
        self.publisher.set_ingest_server(self.server_2)

        # -- Lets check if the server is in the publisher
        self.assertTrue(self.publisher.ingest_server == self.server_2)


    def test_set_invalid_ingest_server(self):
        # -- Make sure server 1 is not an ingest server
        self.server_2.set_mode(ServerMode.RELAY)

        # -- Lets set the ingest server
        self.publisher.set_ingest_server(self.server_2)

        # -- Lets check if the server is in the publisher
        self.assertFalse(self.publisher.ingest_server == self.server_2)

    def test_set_ingest_server_twice(self):
        # -- Make sure server 1 is an ingest server
        self.server_2.set_mode(ServerMode.INGEST)

        # -- Lets set the ingest server
        self.publisher.set_ingest_server(self.server_2)

        # -- Lets set the ingest server again
        self.publisher.set_ingest_server(self.server_2)

        # -- Lets check if the server is in the publisher
        self.assertTrue(self.publisher.ingest_server == self.server_2)


    def test_remove_ingest_server(self):
        # -- Make sure server 1 is an ingest server
        self.server_2.set_mode(ServerMode.INGEST)

        # -- Lets set the ingest server
        self.publisher.set_ingest_server(self.server_2)

        # -- Lets remove the ingest server
        self.publisher.remove_ingest_server()

        # -- Lets check if the server is in the publisher
        self.assertTrue(self.publisher.ingest_server == None)

    def test_remove_ingest_server_twice(self):
        # -- Make sure server 1 is an ingest server
        self.server_1.set_mode(ServerMode.INGEST)

        # -- Lets set the ingest server
        self.publisher.set_ingest_server(self.server_1)

        # -- Lets remove the ingest server
        self.publisher.remove_ingest_server()

        # -- Lets remove the ingest server again
        self.publisher.remove_ingest_server()

        # -- Lets check if the server is in the publisher
        self.assertTrue(self.publisher.ingest_server == None)

    def test_remove_inject_server_not_set(self):
        # -- Lets remove the ingest server
        self.publisher.remove_ingest_server()

        # -- Lets check if the server is in the publisher
        self.assertTrue(self.publisher.ingest_server == None)