import datetime
import secrets
import uuid

class HeartbeatResponse():
    SUCCESS = 0
    TOO_LATE = 1
    TOO_SOON = 2
    TIMED_OUT = 3
    NOT_STARTED = 4
    NOT_FOUND = 5

    def __str__(self) -> str:
        return str(self.value)


class Heartbeat():

    def __init__(
        self, 
        server_id: str,
        interval: int = 5,
        timeout: int = 10,
        timeout_max: int = 3,
        frame_of_error: int = 2, # -- FoE +- the amount of time the server can be late or early by
    ):
        self.started = False
        self.heartbeat_id = uuid.uuid4()
        self.date_created = datetime.datetime.now()

        self.server_id = server_id
        self.interval = interval
        self.timeout = timeout
        self.timeouts = 0
        self.timeout_max = timeout_max
        self.last_beat = datetime.datetime.now()
        self.frame_of_error = frame_of_error
        self.key = self.generate_key()

        # -- add self to the heartbeats dict
        heartbeats[self.server_id] = self



    """
        Generate a new key for the heartbeat
        :name: generate_key
        :return: str - The new key
    """
    def generate_key(self):
        return f'heartbeat_{secrets.token_hex(16)}'

    

    """
        Check if the heartbeat has sent too soon, accounting for frame of error
        :name: has_sent_too_soon
        :return: bool - True if the heartbeat has sent too soon
    """
    def has_sent_too_soon(self):
        return (datetime.datetime.now() - self.last_beat).total_seconds() < self.interval - self.frame_of_error



    """
        Check if the heartbeat has timed out, aka sent too late, accounting for frame of error
        :name: has_sent_too_late
        :return: bool - True if the heartbeat has timed out
    """
    def has_sent_too_late(self):
        return (datetime.datetime.now() - self.last_beat).total_seconds() > self.timeout + self.frame_of_error



    """
        Check if the heartbeat has timed out too many times
        :name: has_timed_out_too_many_times
        :return: bool - True if the heartbeat has timed out too many times
    """
    def has_timed_out_too_many_times(self):
        return self.timeouts >= self.timeout_max



    """
        Check if the heartbeat is still valid
        :name: internal_check
        :return: HeartbeatResponse - The response from the heartbeat
    """
    def internal_check(self) -> HeartbeatResponse:
        # -- Check if the heartbeat has sent too soon
        if self.has_sent_too_soon():
            self.timeout += 1
            return HeartbeatResponse.TOO_SOON

        if self.has_sent_too_late():
            self.timeouts += 1
            return HeartbeatResponse.TOO_LATE
            
        # -- Check if the heartbeat has timed out too many times
        if self.has_timed_out_too_many_times():
            return HeartbeatResponse.TIMED_OUT



    """
        Beat
        :name: beat
        :return: None
    """
    def beat(self) -> HeartbeatResponse:
        
        # -- Check if we have started the heartbeat
        #    If not, start it
        if not self.started:
            self.started = True
            self.last_beat = datetime.datetime.now()
            self.key = self.generate_key()

            return HeartbeatResponse.SUCCESS

        
        # -- Check if the heartbeat is still valid
        if resp := self.internal_check() != HeartbeatResponse.SUCCESS:
            return resp

        
        # -- Update the last beat
        self.last_beat = datetime.datetime.now()
        self.key = self.generate_key()
        return HeartbeatResponse.SUCCESS



    """
        Serialize the heartbeat object
        :name: serialize
        :return: dict - The serialized heartbeat object
    """
    def serialize(self):
        return {
            'server_id': self.server_id,
            'interval': self.interval,
            'timeout': self.timeout,
            'timeouts': self.timeouts,
            'timeout_max': self.timeout_max,
            'last_beat': self.last_beat,
            'key': self.key,
            'started': self.started,
            'heartbeat_id': self.heartbeat_id,
            'date_created': self.date_created,
        }

            

# -- Outof class functionality --
heartbeats = {}



"""
    Get a heartbeat by server id
    :name: get_heartbeat
    :param server_id: str - The server id
    :return: Heartbeat - The heartbeat object or None
"""
def get_heartbeat(server_id: str) -> Heartbeat or None:
    return heartbeats[server_id]



"""
    Get a heartbeat by heartbeat id
    :name: get_heartbeat_by_id
    :param heartbeat_id: str - The heartbeat id
    :return: Heartbeat - The heartbeat object or None
"""
def get_heartbeat_by_id(heartbeat_id: str) -> Heartbeat or None:
    for heartbeat in heartbeats.values():
        if heartbeat.heartbeat_id == heartbeat_id:
            return heartbeat

    return None



"""
    Delete a heartbeat by server id
    :name: delete_heartbeat
    :param server_id: str - The server id
    :return: HeartbeatResponse - The response from the heartbeat
"""
def delete_heartbeat(server_id: str) -> bool:
    if server_id in heartbeats:
        del heartbeats[server_id]
        return HeartbeatResponse.SUCCESS

    return HeartbeatResponse.NOT_FOUND



"""
    Delete a heartbeat by heartbeat id
    :name: delete_heartbeat_by_id
    :param heartbeat_id: str - The heartbeat id
    :return: HeartbeatResponse - The response from the heartbeat
"""
def delete_heartbeat_by_id(heartbeat_id: str) -> bool:
    for heartbeat in heartbeats.values():
        if heartbeat.heartbeat_id == heartbeat_id:
            del heartbeats[heartbeat.server_id]
            return HeartbeatResponse.SUCCESS

    return HeartbeatResponse.NOT_FOUND



"""
    Check health of a heartbeat
    :name: check_health
    :param server_id: str - The server id
    :return: HeartbeatResponse - The response from the heartbeat
"""
def check_health(server_id: str) -> HeartbeatResponse:
    if heartbeat := get_heartbeat(server_id):
        return heartbeat.internal_check()

    return HeartbeatResponse.NOT_FOUND



"""
    Check health of a heartbeat by heartbeat id
    :name: check_health_by_id
    :param heartbeat_id: str - The heartbeat id
    :return: HeartbeatResponse - The response from the heartbeat
"""
def check_health_by_id(heartbeat_id: str) -> HeartbeatResponse:
    if heartbeat := get_heartbeat_by_id(heartbeat_id):
        return heartbeat.internal_check()

    return HeartbeatResponse.NOT_FOUND



"""
    Check all heartbeats health
    :name: check_all_health
    :return: dict - The health of all heartbeats
"""
def check_all_health() -> dict:
    health = {}

    for heartbeat in heartbeats.values():
        health[heartbeat.server_id] = heartbeat.internal_check()

    return health