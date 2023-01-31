from django.test import TestCase

from server_manager.models import Server, Publisher
from server_manager.library import ServerMode
from server_manager.library.server import (
    get_servers_by_mode,
    get_publisher_by_server
)

class ServerLibTest(TestCase):
    def setUp(self):
        self.server_1 = Server.objects.create(
            slug='server-1',
            name='Server 1',
            mode=ServerMode.INGEST.to_string(),
        )

        self.server_2 = Server.objects.create(
            slug='server-2',
            name='Server 2',
            mode=ServerMode.INGEST.to_string(),
        )

        self.server_3 = Server.objects.create(
            slug='server-3',
            name='Server 3',
            mode=ServerMode.INGEST.to_string(),
        )

        self.publisher_1 = Publisher.objects.create(
            name='Publisher 1',
            ingest_server=self.server_1,
        )

        self.publisher_2 = Publisher.objects.create(
            name='Publisher 2',
            ingest_server=self.server_2,
        )

        self.publisher_3 = Publisher.objects.create(
            name='Publisher 3',
            ingest_server=self.server_3,
        )



    def test_get_servers_by_mode(self):
        servers = get_servers_by_mode(ServerMode.INGEST)

        self.assertEqual(len(servers), 3)
        self.assertEqual(servers[0], self.server_1)
        self.assertEqual(servers[1], self.server_2)
        self.assertEqual(servers[2], self.server_3)
    

    def test_get_publisher_by_server(self):
        publishers = get_publisher_by_server(self.server_1)

        self.assertEqual(len(publishers), 1)
        self.assertEqual(publishers[0], self.publisher_1)

        publishers = get_publisher_by_server(self.server_2)

        self.assertEqual(len(publishers), 1)
        self.assertEqual(publishers[0], self.publisher_2)

        publishers = get_publisher_by_server(self.server_3)

        self.assertEqual(len(publishers), 1)
        self.assertEqual(publishers[0], self.publisher_3)


    def test_get_publisher_by_server_no_publisher(self):
        self.publisher_1.delete()

        publishers = get_publisher_by_server(self.server_1)

        self.assertEqual(len(publishers), 0)

        self.publisher_2.delete()

        publishers = get_publisher_by_server(self.server_2)

        self.assertEqual(len(publishers), 0)

        self.publisher_3.delete()

        publishers = get_publisher_by_server(self.server_3)

        self.assertEqual(len(publishers), 0)


    def test_get_publisher_by_server_in_ingest(self):
        self.assertIsNotNone(self.publisher_2.set_ingest_server(self.server_1))
        self.assertIsNotNone(self.publisher_3.set_ingest_server(self.server_1))

        publishers = get_publisher_by_server(self.server_1)

        self.assertEqual(len(publishers), 3)
        self.assertEqual(publishers[0], self.publisher_1)
        self.assertEqual(publishers[1], self.publisher_2)
        self.assertEqual(publishers[2], self.publisher_3)

    
    def test_get_publisher_by_server_in_server_list(self):
        self.publisher_2.set_ingest_server(self.server_1)
        self.server_2.set_mode(ServerMode.RELAY)

        self.publisher_2.add_server(self.server_2)
        self.publisher_3.add_server(self.server_2)

        publishers = get_publisher_by_server(self.server_2)

        self.assertEqual(len(publishers), 2)
        


