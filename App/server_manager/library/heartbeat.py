import datetime
import secrets
import uuid

class HeartbeatResponse():
    SUCCESS = 0
    TOO_LATE = 1
    TOO_SOON = 2
    EXPIRED = 3
    NOT_STARTED = 4
    NOT_FOUND = 5

    def __str__(self) -> str:
        return str(self.value)


class Heartbeat():

    def __init__(
        self, 
        server_id: uuid,
        time_limit: int = 60, # -- The amount of time the server can be late by before it is considered dead
        interval: int = 5,
        timeout: int = 10,
        max_timeouts: int = 3,
        frame_of_error: int = 2, # -- FoE +- the amount of time the server can be late or early by
    ):
        self.started = False
        self.heartbeat_id = uuid.uuid4()
        self.date_created = datetime.datetime.now()

        self.server_id = server_id
        self.interval = interval
        self.timeout = timeout
        self.timeouts = 0
        self.max_timeouts = max_timeouts
        self.last_beat = datetime.datetime.now()
        self.frame_of_error = frame_of_error
        self.key = self.generate_key()
        self.time_limit = time_limit

        # -- Check if the server is already in the heartbeats dict
        #    If so, let's delete it and replace it with this new heartbeat
        if old_hearbeat := get_heartbeat(server_id):
            delete_heartbeat(old_hearbeat)

        # -- add self to the heartbeats dict
        heartbeats[str(self.server_id)] = self


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
        :name: has_EXPIRED_too_many_times
        :return: bool - True if the heartbeat has timed out too many times
    """
    def has_expired_too_many_times(self):
        return self.timeouts >= self.max_timeouts


    """
        Check if the server is dead
        :name: is_server_dead
        :return: bool - True if the server is dead
    """
    def is_server_dead(self):
        return (datetime.datetime.now() - self.last_beat).total_seconds() >= (self.timeout + self.time_limit)


    """
        Check if the heartbeat is still valid
        :name: internal_check
        :return: HeartbeatResponse - The response from the heartbeat
    """
    def internal_check(self) -> HeartbeatResponse:
        # -- Check if the heartbeat has started
        if not self.started:
            return HeartbeatResponse.NOT_STARTED
            
        # -- Check if the server is dead
        if self.is_server_dead():
            return HeartbeatResponse.EXPIRED

        # -- Check if the heartbeat has timed out too many times
        if self.has_expired_too_many_times():
            return HeartbeatResponse.EXPIRED

        return HeartbeatResponse.SUCCESS


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
        if self.internal_check() != HeartbeatResponse.SUCCESS:
            # -- Update the key to prevent any further requests
            #    This instance will be deleted soon by a cleanup task
            self.key = self.generate_key()
            return HeartbeatResponse.EXPIRED

        
        # -- Update the key
        self.key = self.generate_key()


        # -- Check if the heartbeat has sent too soon
        if self.has_sent_too_late():
            self.timeouts += 1
            self.last_beat = datetime.datetime.now()
            return HeartbeatResponse.TOO_LATE

        if self.has_sent_too_soon():
            self.timeouts += 1
            self.last_beat = datetime.datetime.now()
            return HeartbeatResponse.TOO_SOON

        return HeartbeatResponse.SUCCESS




    """
        Serialize the heartbeat object
        :name: serialize
        :return: dict - The serialized heartbeat object
    """
    def serialize(self):
        return {
            'server_id': str(self.server_id),
            'interval': self.interval,
            'timeout': self.timeout,
            'timeouts': self.timeouts,
            'max_timeouts': self.max_timeouts,
            'last_beat': self.last_beat,
            'key': self.key,
            'started': self.started,
            'heartbeat_id': str(self.heartbeat_id),
            'date_created': self.date_created,
        }

            

# -- Outof class functionality --
heartbeats = {}


"""
    Resolves a server id from a heartbeat id
    :name: resolve_server_id
    :param heartbeat_id: uuid - The heartbeat id
    :return: uuid - The server id
"""
def resolve_server_id(heartbeat_id: uuid) -> uuid:
    for server_id, heartbeat in heartbeats.items():
        if heartbeat.heartbeat_id == heartbeat_id:
            return uuid.UUID(server_id)
    return None


"""
    Get a heartbeat by server id
    :name: get_heartbeat
    :param server_id: uuid - The server id
    :return: Heartbeat - The heartbeat object or None
"""
def get_heartbeat(server_id: uuid) -> Heartbeat or None:
    return heartbeats.get(str(server_id), None)



"""
    Get a heartbeat by heartbeat id
    :name: get_heartbeat_by_id
    :param heartbeat_id: uuid - The heartbeat id
    :return: Heartbeat - The heartbeat object or None
"""
def get_heartbeat_by_id(heartbeat_id: uuid) -> Heartbeat or None:
    server_id = resolve_server_id(heartbeat_id)
    if server_id: return get_heartbeat(server_id)
    return None


"""
    Delete a heartbeat by server id
    :name: delete_heartbeat
    :param server_id: uuid - The server id
    :return: HeartbeatResponse - The response from the heartbeat
"""
def delete_heartbeat(server_id: uuid) -> bool:
    if get_heartbeat(server_id):
        del heartbeats[str(server_id)]
        return HeartbeatResponse.SUCCESS

    return HeartbeatResponse.NOT_FOUND



"""
    Delete a heartbeat by heartbeat id
    :name: delete_heartbeat_by_id
    :param heartbeat_id: str - The heartbeat id
    :return: HeartbeatResponse - The response from the heartbeat
"""
def delete_heartbeat_by_id(heartbeat_id: uuid) -> bool:
    server_id = resolve_server_id(heartbeat_id)
    if server_id: return delete_heartbeat(server_id)
    return HeartbeatResponse.NOT_FOUND



"""
    Check health of a heartbeat
    :name: check_health
    :param server_id: uuid - The server id
    :return: HeartbeatResponse - The response from the heartbeat
"""
def check_health(server_id: uuid) -> HeartbeatResponse:
    if heartbeat := get_heartbeat(server_id):
        return heartbeat.internal_check()

    return HeartbeatResponse.NOT_FOUND



"""
    Check health of a heartbeat by heartbeat id
    :name: check_health_by_id
    :param heartbeat_id: uuid - The heartbeat id
    :return: HeartbeatResponse - The response from the heartbeat
"""
def check_health_by_id(heartbeat_id: uuid) -> HeartbeatResponse:
    server_id = resolve_server_id(heartbeat_id)
    if server_id: return check_health(server_id)
    return HeartbeatResponse.NOT_FOUND



"""
    Check all heartbeats health
    :name: check_all_health
    :return: dict - The health of all heartbeats
"""
def check_all_health() -> dict:
    health = {}

    for heartbeat in heartbeats.values():
        health[str(heartbeat.server_id)] = heartbeat.internal_check()

    return health