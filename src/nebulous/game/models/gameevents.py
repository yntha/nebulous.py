from dataclasses import dataclass

from nebulous.game.enums import GameEventType, ChargeType


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


@dataclass
class EatCakeEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player eats a cake.

    Attributes:
        plasma_amount (int): The amount of plasma that was rewarded.
        xp_amount (int): The amount of XP that was rewarded.
    """
    plasma_amount: int  # 3 bytes, encoded
    xp_amount: int  # 3 bytes, encoded


@dataclass
class CoinCountEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player's coin count is updated.

    Attributes:
        player_id (int): The ID of the player that triggered the event.
        coin_count (int): The new coin count of the player.
    """
    player_id: int  # 1 byte
    coin_count: int  # 2 bytes


@dataclass
class SpeedEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player uses the speed ability.

    Attributes:
        speed_time_ms_offset (int): The offset in milliseconds when the speed ability
            expires. This is used to calculate the duration of the speed ability.
    """
    speed_time_ms_offset: int  # 2 bytes


@dataclass
class TrickEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player does a trick.

    Attributes:
        trick_id (int): The ID of the trick that was performed.
        trick_score (int): The score that was earned from the trick.
        trick_xp (int): The XP that was earned from the trick.
    """
    trick_id: int  # 1 byte
    trick_score: int  # 2 bytes
    trick_xp: int  # 3 bytes, encoded


@dataclass
class AccoladeEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player earns an accolade.

    Attributes:
        accolades_gained (int): The number of accolades that were gained.
    """
    accolades_gained: int  # 1 byte


@dataclass
class InvisibleEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player uses the ghost ability.

    Attributes:
        ghost_time_ms_offset (int): The offset in milliseconds when the ghost ability
            expires. This is used to calculate the duration of the ghost ability.
    """
    ghost_time_ms_offset: int  # 2 bytes


@dataclass
class KilledByEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player is killed by another
    player.

    Attributes:
        killer_id (int): The ID of the player that killed the player.
    """
    killer_id: int


@dataclass
class RadiationCloudEvent(GameEvent):
    """
    Represents a triggered event that occurs when a radiation cloud has spawned
    in the game.

    Attributes:
        player_id (int): The ID of the player that triggered the rad cloud.
        x_pos (float): The X position of the radiation cloud.
        y_pos (float): The Y position of the radiation cloud.
        time_remaining (float): The time remaining for the radiation cloud to
            expire.
    """
    player_id: int  # 1 byte
    x_pos: float  # 3 bytes, encoded, clamped to map size
    y_pos: float  # 3 bytes, encoded, clamped to map size
    time_remaining: float  # 1 byte, encoded, clamped to 16.0


@dataclass
class ChargeEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player begins to charge up.
    This event is only triggered in the Charge game mode.

    Attributes:
        player_id (int): The ID of the player that triggered the event.
        charge_type (ChargeType): The type of the charge up.
    """
    player_id: int  # 1 byte
    charge_type: ChargeType  # 1 byte


@dataclass
class LPCountEvent(GameEvent):
    """
    Represents a triggered event that occurs when the LP count is updated or set.
    The purpose of this event isn't so clear. It sets a variable in the game that
    holds the current number of active(joined) players in the current session.

    Attributes:
        lp_count (int): The new LP count.
    """
    lp_count: int  # 1 byte


@dataclass
class BRBoundsEvent(GameEvent):
    """
    Represents a triggered event that occurs when the Battle Royale bounds are updated.
    This event is only triggered in the Battle Royale game mode.

    Attributes:
        bounds_left (float): The left bound of the BR area.
        bounds_top (float): The top bound of the BR area.
        bounds_right (float): The right bound of the BR area.
        bounds_bottom (float): The bottom bound of the BR area.
        lim_bounds_left (float): The left bound of the limited BR area.
        lim_bounds_top (float): The top bound of the limited BR area.
        lim_bounds_right (float): The right bound of the limited BR area.
        lim_bounds_bottom (float): The bottom bound of the limited BR area.
    """
    bounds_left: float  # 3 bytes, encoded, clamped to map size
    bounds_top: float  # 3 bytes, encoded, clamped to map size
    bounds_right: float  # 3 bytes, encoded, clamped to map size
    bounds_bottom: float  # 3 bytes, encoded, clamped to map size
    lim_bounds_left: float  # 3 bytes, encoded, clamped to map size
    lim_bounds_top: float  # 3 bytes, encoded, clamped to map size
    lim_bounds_right: float  # 3 bytes, encoded, clamped to map size
    lim_bounds_bottom: float  # 3 bytes, encoded, clamped to map size


EventMap = {
    GameEventType.UNKNOWN: GameEvent,
    GameEventType.EAT_DOTS: GameEvent,
    GameEventType.EAT_BLOB: GameEvent,
    GameEventType.EAT_SMBH: GameEvent,
    GameEventType.BLOB_EXPLODE: BlobExplodeEvent,
    GameEventType.BLOB_LOST: GameEvent,
    GameEventType.EJECT: EjectEvent,
    GameEventType.SPLIT: SplitEvent,
    GameEventType.RECOMBINE: RecombineEvent,
    GameEventType.TIMER_WARNING: GameEvent,
    GameEventType.CTF_SCORE: GameEvent,
    GameEventType.CTF_FLAG_RETURNED: GameEvent,
    GameEventType.CTF_FLAG_STOLEN: GameEvent,
    GameEventType.CTF_FLAG_DROPPED: GameEvent,
    GameEventType.ACHIEVEMENT_EARNED: AchievementEarnedEvent,
    GameEventType.XP_GAINED: GameEvent,
    GameEventType.UNUSED_2: GameEvent,
    GameEventType.XP_SET: XPSetEvent,
    GameEventType.DQ_SET: DQSetEvent,
    GameEventType.DQ_COMPLETED: DQCompletedEvent,
    GameEventType.DQ_PROGRESS: DQProgressEvent,
    GameEventType.EAT_SERVER_BLOB: GameEvent,
    GameEventType.EAT_SPECIAL_OBJECTS: EatSOEvent,
    GameEventType.SO_SET: SetSOEvent,
    GameEventType.LEVEL_UP: LevelUpEvent,
    GameEventType.ARENA_RANK_ACHIEVED: ArenaRankAchievedEvent,
    GameEventType.DOM_CP_LOST: GameEvent,
    GameEventType.DOM_CP_GAINED: GameEvent,
    GameEventType.UNUSED_1: GameEvent,
    GameEventType.CTF_GAINED: GameEvent,
    GameEventType.GAME_OVER: GameEvent,
    GameEventType.BLOB_STATUS: BlobStatusEvent,
    GameEventType.TELEPORT: TeleportEvent,
    GameEventType.SHOOT: ShootEvent,
    GameEventType.CLAN_WAR_WON: ClanWarWonEvent,
    GameEventType.PLASMA_REWARD: PlasmaRewardEvent,
    GameEventType.EMOTE: EmoteEvent,
    GameEventType.END_MISSION: EndMissionEvent,
    GameEventType.XP_GAINED_2: XPGained2Event,
    GameEventType.EAT_CAKE: EatCakeEvent,
    GameEventType.COIN_COUNT: CoinCountEvent,
    GameEventType.CLEAR_EFFECTS: GameEvent,
    GameEventType.SPEED: SpeedEvent,
    GameEventType.TRICK: TrickEvent,
    GameEventType.DESTROY_ASTEROID: GameEvent,
    GameEventType.ACCOLADE: AccoladeEvent,
    GameEventType.INVIS: InvisibleEvent,
    GameEventType.KILLED_BY: KilledByEvent,
    GameEventType.RADIATION_CLOUD: RadiationCloudEvent,
    GameEventType.CHARGE: GameEvent,  # Implement these events as well
    GameEventType.LP_COUNT: GameEvent,
    GameEventType.BR_BOUNDS: GameEvent,
    GameEventType.MINIMAP: GameEvent,
    GameEventType.RLGL_DEATH: GameEvent,
    GameEventType.RLGL_STATE: GameEvent,
}


__all__ = [
    "GameEvent",
    "BlobExplodeEvent",
    "EjectEvent",
    "SplitEvent",
    "RecombineEvent",
    "AchievementEarnedEvent",
    "XPSetEvent",
    "DQSetEvent",
    "DQCompletedEvent",
    "DQProgressEvent",
    "EatSOEvent",
    "SetSOEvent",
    "LevelUpEvent",
    "ArenaRankAchievedEvent",
    "BlobStatusEvent",
    "TeleportEvent",
    "ShootEvent",
    "ClanWarWonEvent",
    "PlasmaRewardEvent",
    "EmoteEvent",
    "EndMissionEvent",
    "XPGained2Event",
    "EatCakeEvent",
    "CoinCountEvent",
    "SpeedEvent",
    "TrickEvent",
    "AccoladeEvent",
    "InvisibleEvent",
    "KilledByEvent",
    "RadiationCloudEvent",
]
