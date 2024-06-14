from dataclasses import dataclass

from nebulous.game.enums import GameEventType


@dataclass
class GameEvent:
    """
    Represents a game event that can be triggered by in-game actions.

    Attributes:
        event_type (GameEventType): The type of event that was triggered.
    """
    event_type: GameEventType


@dataclass
class BlobExplodeEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player blob explodes.

    Attributes:
        player_id (int): The ID of the player that triggered the event.
        blob_id (int): The ID of the player blob that exploded.
    """
    player_id: int  # 1 byte
    blob_id: int  # 1 byte


@dataclass
class EjectEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player ejects mass.

    Attributes:
        player_id (int): The ID of the player that triggered the event.
        blob_id (int): The ID of the player blob that ejected mass.
    """
    player_id: int  # 1 byte
    blob_id: int  # 1 byte


@dataclass
class SplitEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player splits.

    Attributes:
        player_id (int): The ID of the player that triggered the event.
    """
    player_id: int  # 1 byte


@dataclass
class RecombineEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player recombines.

    Attributes:
        player_id (int): The ID of the player that triggered the event.
    """
    player_id: int
