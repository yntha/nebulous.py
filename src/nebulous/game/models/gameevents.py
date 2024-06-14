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
    player_id: int  # 1 byte


@dataclass
class AchievementEarnedEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player earns an achievement.

    Attributes:
        achievement_id (int): The ID of the achievement that was earned.
    """
    achievement_id: int  # 2 bytes


@dataclass
class XPSetEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player's XP is set or updated
    with tempboosts. Click type is not specified here, but plasma boost is, but
    plasma boost duration is not specified. This protocol is such a mess.

    Attributes:
        player_xp (int): The player's new XP value.
        xp_mult_type (int): The type of XP boost that was set.
        xp_duration_s (int): The duration of the XP boost in seconds.
        plasma_boost_type (int): The type of plasma boost that was set.
        click_type_duration_s (int): The duration of the click type in seconds.
    """
    player_xp: int  # 8 bytes
    xp_mult_type: int  # 1 byte
    xp_duration_s: int  # 4 bytes
    plasma_boost_type: int  # 1 byte
    click_type_duration_s: int  # 4 bytes


@dataclass
class DQSetEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player's DQ(Daily Quest)
    is set or updated.

    Attributes:
        dq_id (int): The ID of the daily quest that was set.
        completed (bool): Whether the daily quest was completed.
    """
    dq_id: int
    completed: bool


@dataclass
class DQCompletedEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player completes a daily quest.

    Attributes:
        dq_id (int): The ID of the daily quest that was completed.
    """
    dq_id: int


@dataclass
class DQProgressEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player's daily quest progress
    is updated.

    Attributes:
        progress (int): The new progress value of the daily quest.
    """
    progress: int
