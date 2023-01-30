from accounts.models import Member
from django.test import TestCase
from server_manager.library import ServerMode
from server_manager.models import Server

class PublisherTest(TestCase):

    def setUp(self):
        self.server_1 = Server.objects.create(
            slug='server-1',
            name='Server 1',
            mode=ServerMode.INGEST,
        )

        self.server_2 = Server.objects.create(
            slug='server-2',
            name='Server 2',
            mode=ServerMode.INGEST,
        )

        self.server_3 = Server.objects.create(
            slug='server-3',
            name='Server 3',
            mode=ServerMode.INGEST,
        )


    def test_announce(self):
        ip = '154.87.23.75'
        port = 1234

        # TODO: Fully implement this test once the 
        #       announce function is implemented
        hb_id = '1234567890'

        self.server_1.announce(ip, port, hb_id)

        self.assertEqual(self.server_1.ip, ip)
        self.assertEqual(self.server_1.port, port)
        # self.assertEqual(self.server_1.hb_id, hb_id)

    def test_announce_invalid_ip(self):
        ip = 'dsgf'
        port = 1234
        hb_id = '1234567890'

        with self.assertRaises(ValueError):
            self.server_1.announce(ip, port, hb_id)
        
    def test_announce_invalid_port(self):
        ip = '154.43.66.43'
        port = 123456
        hb_id = '1234567890'

        with self.assertRaises(ValueError):
            self.server_1.announce(ip, port, hb_id)

        