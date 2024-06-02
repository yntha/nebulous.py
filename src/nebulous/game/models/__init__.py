from dataclasses import dataclass
from enum import Enum

from nebulous.game.models.client import Client


@dataclass
class ServerData:
    client_id: int = 0
    client_id2: int = 0
    public_id: int = 0
    private_id: int = 0


class ClientState(Enum):
    CONNECTING = 0
    CONNECTED = 1
    DISCONNECTING = 2
    DISCONNECTED = 3


__all__ = ["Client", "ServerData", "ClientState"]
