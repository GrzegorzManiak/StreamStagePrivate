from enum import Enum

class ServerMode(Enum):
    INGEST = 1
    RELAY = 2
    ROOT_RELAY = 3

    def to_string(self) -> str or None:
        match self:
            case ServerMode.INGEST: return 'I'
            case ServerMode.RELAY: return 'R'
            case ServerMode.ROOT_RELAY: return 'RR'

        return None

    def from_string(mode: str) -> any or None:
        match mode:
            case 'I': return ServerMode.INGEST
            case 'R': return ServerMode.RELAY
            case 'RR': return ServerMode.ROOT_RELAY

        return None