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
    click_type_duration_s: int  # 3 bytes, encoded


@dataclass
class DQSetEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player's DQ(Daily Quest)
    is set or updated.

    Attributes:
        dq_id (int): The ID of the daily quest that was set.
        completed (bool): Whether the daily quest was completed.
    """
    dq_id: int  # 1 byte
    completed: bool  # 1 byte


@dataclass
class DQCompletedEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player completes a daily quest.

    Attributes:
        dq_id (int): The ID of the daily quest that was completed.
    """
    dq_id: int  # 1 byte


@dataclass
class DQProgressEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player's daily quest progress
    is updated.

    Attributes:
        progress (int): The new progress value of the daily quest.
    """
    progress: int  # 2 bytes


@dataclass
class EatSOEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player eats a special object.

    Attributes:
        so_id (int): The ID of the special object that was eaten.
        so_count (int): The number of special objects that were eaten.
    """
    so_id: int  # 1 byte
    so_count: int  # 1 byte


@dataclass
class SetSOEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player's special object count
    is set.

    Attributes:
        so_id (int): The ID of the special object that was set.
        so_count (int): The new special object count.
    """
    so_id: int  # 1 byte
    so_count: int  # 4 bytes


@dataclass
class LevelUpEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player levels up.

    Attributes:
        level (int): The new level of the player.
    """
    level: int  # 2 bytes


@dataclass
class ArenaRankAchievedEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player achieves a new arena rank.

    Attributes:
        achieved_rank (bool): Whether the player achieved the rank. Unsure if this
            is a correct title for this field. In the game, it's only checked to see
            if it's equal to 1.
        rank (int): The new arena rank of the player.
    """
    achieved_rank: bool  # 1 byte
    rank: int  # 1 byte


@dataclass
class BlobStatusEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player blob status is updated.

    Attributes:
        player_id (int): The ID of the player that triggered the event.
        blob_id (int): The ID of the player blob that was updated.
        status (int): The status of the player blob.
    """
    player_id: int  # 1 byte
    blob_id: int  # 1 byte
    status: int  # 2 bytes


@dataclass
class TeleportEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player teleports.

    Attributes:
        player_id (int): The ID of the player that triggered the event.
    """
    player_id: int  # 1 byte


@dataclass
class ShootEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player blob shoots a spell.

    Attributes:
        player_id (int): The ID of the player that triggered the event.
        blob_id (int): The ID of the player blob that shot the spell.
        spell_id (int): The ID(type) of the spell that was shot.
    """
    player_id: int  # 1 byte
    blob_id: int  # 1 byte
    spell_id: int  # 1 byte


@dataclass
class ClanWarWonEvent(GameEvent):
    """
    Represents a triggered event that occurs when a clan war has concluded.

    Attributes:
        reward (int): The reward that was given to the player. It is doubled
            for the winning clan.
    """
    reward: int  # 2 bytes


@dataclass
class PlasmaRewardEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player receives a plasma
    reward.

    Attributes:
        reward (int): The amount of plasma that was rewarded.
        multiplier (int): The plasma reward multiplier.
    """
    reward: int  # 3 bytes, encoded
    multiplier: int  # 1 byte


@dataclass
class EmoteEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player blob sends an emote.

    Attributes:
        player_id (int): The ID of the player that triggered the event.
        blob_id (int): The ID of the player blob that sent the emote.
        emote_id (int): The ID of the emote that was sent.
        custom_emote_id (int): The ID of the custom emote that was sent, if any.
    """
    player_id: int  # 1 byte
    blob_id: int  # 1 byte
    emote_id: int  # 1 byte
    custom_emote_id: int  # 4 bytes


@dataclass
class EndMissionEvent(GameEvent):
    """
    Represents a triggered event that occurs when a campaign mission has
    ended.

    Attributes:
        mission_id (int): The ID of the mission that ended.
        passed (bool): Whether the mission was passed.
        next_mission_id (int): The ID of the next mission.
        xp_reward (int): The XP reward for completing the mission.
        plasma_reward (int): The plasma reward for completing the mission.
    """
    mission_id: int  # 1 byte
    passed: bool  # 1 byte
    next_mission_id: int  # 1 byte
    xp_reward: int  # 3 bytes, encoded
    plasma_reward: int  # 2 bytes


@dataclass
class XPGained2Event(GameEvent):
    """
    Represents a triggered event that occurs when the current player gains XP,
    either from eating mass, dots, or from other sources.

    Attributes:
        player_xp (int): The player's XP value for this session.
        xp_chain_multiplier (float): The XP chain multiplier. This is the text
            which appears under the XP gained text in-game. E.g. "x2.25".
        xp_gained (int): The amount of XP that was gained.
    """
    player_xp: int  # 3 bytes, encoded
    xp_chain_multiplier: float  # 2 bytes, encoded
    xp_gained: int  # 3 bytes, encoded
