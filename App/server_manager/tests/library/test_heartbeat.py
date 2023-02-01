from django.test import TestCase
import datetime
import uuid

from server_manager.library import (
    Heartbeat,
    HeartbeatResponse,
    heartbeats,
    get_heartbeat,
    delete_heartbeat,
    check_health,
    resolve_server_id,
)

class HeartbeatLibTest(TestCase):
    def setUp(self):
        self.heartbeats = []
        self.TOTAL_HEARTBEATS = 5

        for _ in range(self.TOTAL_HEARTBEATS):
            self.heartbeats.append(Heartbeat(uuid.uuid4()))


    # -- Create heartbeat
    def test_create_heartbeat(self):
        heartbeat = Heartbeat(uuid.uuid4())
        self.assertTrue(heartbeat in heartbeats.values())

    def test_multiple_create_heartbeat(self):
        hb_id = uuid.uuid4()

        heartbeat_1 = Heartbeat(hb_id)

        self.assertTrue(heartbeat_1 in heartbeats.values())
        self.assertTrue(heartbeat_1 == get_heartbeat(hb_id))

        heartbeat_2 = Heartbeat(hb_id)

        self.assertTrue(heartbeat_2 in heartbeats.values())
        self.assertTrue(heartbeat_2 == get_heartbeat(hb_id))

        # -- Now make sure that the first heartbeat is gone
        self.assertFalse(heartbeat_1 in heartbeats.values())


    # -- Resolve heartbeat
    def test_resolve_heartbeat(self):
        for heartbeat in self.heartbeats:
            self.assertTrue(heartbeat.server_id == resolve_server_id(heartbeat.heartbeat_id))

    def test_resolve_heartbeat_invalid_id(self):
        self.assertTrue(resolve_server_id(uuid.uuid4()) == None)
        

    # -- Get heartbeat
    def test_get_heartbeat(self):
        for heartbeat in self.heartbeats:
            self.assertTrue(heartbeat == get_heartbeat(heartbeat.server_id))
            
    def test_get_heartbeat_invalid_id(self):
        self.assertTrue(get_heartbeat(uuid.uuid4()) == None)



    # -- Delete heartbeat
    def test_delete_heartbeat(self):
        for heartbeat in self.heartbeats:
            self.assertTrue(delete_heartbeat(heartbeat.server_id) == HeartbeatResponse.SUCCESS)
            self.assertTrue(heartbeat not in heartbeats.values())

    def test_delete_heartbeat_invalid_id(self):
        self.assertTrue(delete_heartbeat(uuid.uuid4()) == HeartbeatResponse.NOT_FOUND)


    # -- Check health
    def test_check_health(self):
        for heartbeat in self.heartbeats:
            self.assertTrue(check_health(heartbeat.server_id) == HeartbeatResponse.NOT_STARTED)

        # -- Start the heartbeats
        for heartbeat in self.heartbeats:
            heartbeat.beat()

        # -- Now check the health
        for heartbeat in self.heartbeats:
            self.assertTrue(check_health(heartbeat.server_id) == HeartbeatResponse.SUCCESS)

        # -- Go back 15 seconds
        new_time = datetime.datetime.now() - datetime.timedelta(seconds=25)

        # -- Now check the health
        for heartbeat in self.heartbeats:
            heartbeat.last_beat = new_time
            # -- Beat again, too late
            self.assertTrue(heartbeat.beat() == HeartbeatResponse.TOO_LATE)

            # -- One timeout
            self.assertEqual(heartbeat.timeouts, 1)
    
            # -- Beat again, too soon
            self.assertTrue(heartbeat.beat() == HeartbeatResponse.TOO_SOON)

            # -- Should have two timeouts
            self.assertEqual(heartbeat.timeouts, 2)

            # -- Set timeout to the max
            heartbeat.timeouts = heartbeat.max_timeouts

            # -- Check health
            self.assertTrue(check_health(heartbeat.server_id) == HeartbeatResponse.EXPIRED)

            # -- Beat again, should be expired
            self.assertTrue(heartbeat.beat() == HeartbeatResponse.EXPIRED)


    def test_for_death(self):
        for heartbeat in self.heartbeats:
            heartbeat.beat()

            self.assertTrue(check_health(heartbeat.server_id) == HeartbeatResponse.SUCCESS)

            # -- Go forward by the time_limit
            new_time = datetime.datetime.now() - datetime.timedelta(seconds=(
                heartbeat.time_limit + heartbeat.timeout + 1)
            )

            heartbeat.last_beat = new_time
            self.assertTrue(check_health(heartbeat.server_id) == HeartbeatResponse.EXPIRED)


    def test_check_health_invalid_id(self):
        self.assertTrue(check_health(uuid.uuid4()) == HeartbeatResponse.NOT_FOUND)

    