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
