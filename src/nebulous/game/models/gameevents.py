from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from datastream import DeserializingStream
from nebulous.game.enums import GameEventType, ChargeType, RLGLState
from nebulous.game.natives import CompressedInteger, CompressedFloat

if TYPE_CHECKING:
    from nebulous.game.models.client import Client


@dataclass
class GameEvent:
    """
    Represents a game event that can be triggered by in-game actions.

    Attributes:
        event_type (GameEventType): The type of event that was triggered.
    """

    event_type: GameEventType  # 1 byte

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> GameEvent:
        """
        Reads a game event from the given stream.

        Args:
            client (Client): The current client instance.
            stream (DeserializingStream): The stream to read from.

        Returns:
            GameEvent: The game event that was read.
        """
        event_type = GameEventType(stream.read_uint8())

        if event_type not in EventMap:
            client.logger.warning(f"Unknown GameUpdate event type: {event_type}")
            event_type = GameEventType.UNKNOWN
        else:
            client.logger.debug(f"Received GameUpdate event: {event_type}")

        return cls(event_type=event_type)


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> BlobExplodeEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.BLOB_EXPLODE:
            raise ValueError(f"Invalid event type: {event_type}")

        player_id = stream.read_int8()
        blob_id = stream.read_int8()

        client.logger.debug(f"Received BlobExplode event: player_id={player_id}, blob_id={blob_id}")

        return cls(event_type=GameEventType.BLOB_EXPLODE, player_id=player_id, blob_id=blob_id)


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> EjectEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.EJECT:
            raise ValueError(f"Invalid event type: {event_type}")

        player_id = stream.read_int8()
        blob_id = stream.read_int8()

        client.logger.debug(f"Received Eject event: player_id={player_id}, blob_id={blob_id}")

        return cls(event_type=GameEventType.EJECT, player_id=player_id, blob_id=blob_id)


@dataclass
class SplitEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player splits.

    Attributes:
        player_id (int): The ID of the player that triggered the event.
    """

    player_id: int  # 1 byte

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> SplitEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.SPLIT:
            raise ValueError(f"Invalid event type: {event_type}")

        player_id = stream.read_int8()

        client.logger.debug(f"Received Split event: player_id={player_id}")

        return cls(event_type=GameEventType.SPLIT, player_id=player_id)


@dataclass
class RecombineEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player recombines.

    Attributes:
        player_id (int): The ID of the player that triggered the event.
    """

    player_id: int  # 1 byte

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> RecombineEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.RECOMBINE:
            raise ValueError(f"Invalid event type: {event_type}")

        player_id = stream.read_int8()

        client.logger.debug(f"Received Recombine event: player_id={player_id}")

        return cls(event_type=GameEventType.RECOMBINE, player_id=player_id)


@dataclass
class AchievementEarnedEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player earns an achievement.

    Attributes:
        achievement_id (int): The ID of the achievement that was earned.
    """

    achievement_id: int  # 2 bytes

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> AchievementEarnedEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.ACHIEVEMENT_EARNED:
            raise ValueError(f"Invalid event type: {event_type}")

        achievement_id = stream.read_int16()

        client.logger.debug(f"Received AchievementEarned event: achievement_id={achievement_id}")

        return cls(event_type=GameEventType.ACHIEVEMENT_EARNED, achievement_id=achievement_id)


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> XPSetEvent:
        event_type = stream.read_uint8()

        if event_type != GameEventType.XP_SET:
            raise ValueError(f"Invalid event type: {event_type}")

        player_xp = stream.read_int64()
        xp_mult_type = stream.read_int8()
        xp_duration_s = stream.read_int32()
        plasma_boost_type = stream.read_int8()
        click_type_duration_s = CompressedInteger.decompress_from_stream3(stream)

        client.logger.debug(
            f"Received XPSet event: player_xp={player_xp}, xp_mult_type={xp_mult_type}, "
            f"xp_duration_s={xp_duration_s}, plasma_boost_type={plasma_boost_type}, "
            f"click_type_duration_s={click_type_duration_s}"
        )

        return cls(
            event_type=GameEventType.XP_SET,
            player_xp=player_xp,
            xp_mult_type=xp_mult_type,
            xp_duration_s=xp_duration_s,
            plasma_boost_type=plasma_boost_type,
            click_type_duration_s=click_type_duration_s,
        )


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> DQSetEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.DQ_SET:
            raise ValueError(f"Invalid event type: {event_type}")

        dq_id = stream.read_int8()
        completed = stream.read_bool()

        client.logger.debug(f"Received DQSet event: dq_id={dq_id}, completed={completed}")

        return cls(event_type=GameEventType.DQ_SET, dq_id=dq_id, completed=completed)


@dataclass
class DQCompletedEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player completes a daily quest.

    Attributes:
        dq_id (int): The ID of the daily quest that was completed.
    """

    dq_id: int  # 1 byte

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> DQCompletedEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.DQ_COMPLETED:
            raise ValueError(f"Invalid event type: {event_type}")

        dq_id = stream.read_int8()

        client.logger.debug(f"Received DQCompleted event: dq_id={dq_id}")

        return cls(event_type=GameEventType.DQ_COMPLETED, dq_id=dq_id)


@dataclass
class DQProgressEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player's daily quest progress
    is updated.

    Attributes:
        progress (int): The new progress value of the daily quest.
    """

    progress: int  # 2 bytes

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> DQProgressEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.DQ_PROGRESS:
            raise ValueError(f"Invalid event type: {event_type}")

        progress = stream.read_int16()

        client.logger.debug(f"Received DQProgress event: progress={progress}")

        return cls(event_type=GameEventType.DQ_PROGRESS, progress=progress)


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> EatSOEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.EAT_SPECIAL_OBJECTS:
            raise ValueError(f"Invalid event type: {event_type}")

        so_id = stream.read_int8()
        so_count = stream.read_int8()

        client.logger.debug(f"Received EatSpecialObjects event: so_id={so_id}, so_count={so_count}")

        return cls(event_type=GameEventType.EAT_SPECIAL_OBJECTS, so_id=so_id, so_count=so_count)


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> SetSOEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.SO_SET:
            raise ValueError(f"Invalid event type: {event_type}")

        so_id = stream.read_int8()
        so_count = stream.read_int32()

        client.logger.debug(f"Received SetSpecialObjects event: so_id={so_id}, so_count={so_count}")

        return cls(event_type=GameEventType.SO_SET, so_id=so_id, so_count=so_count)


@dataclass
class LevelUpEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player levels up.

    Attributes:
        level (int): The new level of the player.
    """

    level: int  # 2 bytes

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> LevelUpEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.LEVEL_UP:
            raise ValueError(f"Invalid event type: {event_type}")

        level = stream.read_int16()

        client.logger.debug(f"Received LevelUp event: level={level}")

        return cls(event_type=GameEventType.LEVEL_UP, level=level)


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> ArenaRankAchievedEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.ARENA_RANK_ACHIEVED:
            raise ValueError(f"Invalid event type: {event_type}")

        achieved_rank = stream.read_bool()
        rank = stream.read_int8()

        client.logger.debug(f"Received ArenaRankAchieved event: achieved_rank={achieved_rank}, rank={rank}")

        return cls(event_type=GameEventType.ARENA_RANK_ACHIEVED, achieved_rank=achieved_rank, rank=rank)


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
    status: int  # 2 bytes, this is most likely a 16-bit bitfield

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> BlobStatusEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.BLOB_STATUS:
            raise ValueError(f"Invalid event type: {event_type}")

        player_id = stream.read_int8()
        blob_id = stream.read_int8()
        status = stream.read_int16()

        client.logger.debug(
            f"Received BlobStatus event: player_id={player_id}, blob_id={blob_id}," f"status(binary)={status:016b}"
        )

        return cls(event_type=GameEventType.BLOB_STATUS, player_id=player_id, blob_id=blob_id, status=status)


@dataclass
class TeleportEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player teleports.

    Attributes:
        player_id (int): The ID of the player that triggered the event.
    """

    player_id: int  # 1 byte

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> TeleportEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.TELEPORT:
            raise ValueError(f"Invalid event type: {event_type}")

        player_id = stream.read_int8()

        client.logger.debug(f"Received Teleport event: player_id={player_id}")

        return cls(event_type=GameEventType.TELEPORT, player_id=player_id)


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> ShootEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.SHOOT:
            raise ValueError(f"Invalid event type: {event_type}")

        player_id = stream.read_int8()
        blob_id = stream.read_int8()
        spell_id = stream.read_int8()

        client.logger.debug(f"Received Shoot event: player_id={player_id}, blob_id={blob_id}, spell_id={spell_id}")

        return cls(event_type=GameEventType.SHOOT, player_id=player_id, blob_id=blob_id, spell_id=spell_id)


@dataclass
class ClanWarWonEvent(GameEvent):
    """
    Represents a triggered event that occurs when a clan war has concluded.

    Attributes:
        reward (int): The reward that was given to the player. It is doubled
            for the winning clan.
    """

    reward: int  # 2 bytes

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> ClanWarWonEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.CLAN_WAR_WON:
            raise ValueError(f"Invalid event type: {event_type}")

        reward = stream.read_int16()

        client.logger.debug(f"Received ClanWarWon event: reward={reward}")

        return cls(event_type=GameEventType.CLAN_WAR_WON, reward=reward)


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> PlasmaRewardEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.PLASMA_REWARD:
            raise ValueError(f"Invalid event type: {event_type}")

        reward = CompressedInteger.decompress_from_stream3(stream)
        multiplier = stream.read_int8()

        client.logger.debug(f"Received PlasmaReward event: reward={reward}, multiplier={multiplier}")

        return cls(event_type=GameEventType.PLASMA_REWARD, reward=reward, multiplier=multiplier)


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> EmoteEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.EMOTE:
            raise ValueError(f"Invalid event type: {event_type}")

        player_id = stream.read_int8()
        blob_id = stream.read_int8()
        emote_id = stream.read_int8()
        custom_emote_id = stream.read_int32()

        client.logger.debug(
            f"Received Emote event: player_id={player_id}, blob_id={blob_id}, emote_id={emote_id}, "
            f"custom_emote_id={custom_emote_id}"
        )

        return cls(
            event_type=GameEventType.EMOTE,
            player_id=player_id,
            blob_id=blob_id,
            emote_id=emote_id,
            custom_emote_id=custom_emote_id,
        )


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> EndMissionEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.END_MISSION:
            raise ValueError(f"Invalid event type: {event_type}")

        mission_id = stream.read_int8()
        passed = stream.read_bool()
        next_mission_id = stream.read_int8()
        xp_reward = CompressedInteger.decompress_from_stream3(stream)
        plasma_reward = stream.read_int16()

        client.logger.debug(
            f"Received EndMission event: mission_id={mission_id}, passed={passed}, next_mission_id={next_mission_id}, "
            f"xp_reward={xp_reward}, plasma_reward={plasma_reward}"
        )

        return cls(
            event_type=GameEventType.END_MISSION,
            mission_id=mission_id,
            passed=passed,
            next_mission_id=next_mission_id,
            xp_reward=xp_reward,
            plasma_reward=plasma_reward,
        )


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
    xp_chain_multiplier: float  # 2 bytes, encoded, clamped to 8.0
    xp_gained: int  # 3 bytes, encoded

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> XPGained2Event:
        event_type = stream.read_int8()

        if event_type != GameEventType.XP_GAINED_2:
            raise ValueError(f"Invalid event type: {event_type}")

        player_xp = CompressedInteger.decompress_from_stream3(stream)
        xp_chain_multiplier = CompressedFloat.from_stream(8.0, stream).value
        xp_chain_multiplier += 1.0
        xp_gained = CompressedInteger.decompress_from_stream3(stream)

        client.logger.debug(
            f"Received XPGained2 event: player_xp={player_xp}, xp_chain_multiplier={xp_chain_multiplier}, "
            f"xp_gained={xp_gained}"
        )

        return cls(
            event_type=GameEventType.XP_GAINED_2,
            player_xp=player_xp,
            xp_chain_multiplier=xp_chain_multiplier,
            xp_gained=xp_gained,
        )


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> EatCakeEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.EAT_CAKE:
            raise ValueError(f"Invalid event type: {event_type}")

        plasma_amount = CompressedInteger.decompress_from_stream3(stream)
        xp_amount = CompressedInteger.decompress_from_stream3(stream)

        client.logger.debug(f"Received EatCake event: plasma_amount={plasma_amount}, xp_amount={xp_amount}")

        return cls(event_type=GameEventType.EAT_CAKE, plasma_amount=plasma_amount, xp_amount=xp_amount)


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> CoinCountEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.COIN_COUNT:
            raise ValueError(f"Invalid event type: {event_type}")

        player_id = stream.read_int8()
        coin_count = stream.read_int16()

        client.logger.debug(f"Received CoinCount event: player_id={player_id}, coin_count={coin_count}")

        return cls(event_type=GameEventType.COIN_COUNT, player_id=player_id, coin_count=coin_count)


@dataclass
class SpeedEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player uses the speed ability.

    Attributes:
        speed_time_ms_offset (int): The offset in milliseconds when the speed ability
            expires. This is used to calculate the duration of the speed ability.
    """

    speed_time_ms_offset: int  # 2 bytes

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> SpeedEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.SPEED:
            raise ValueError(f"Invalid event type: {event_type}")

        speed_time_ms_offset = stream.read_int16()

        client.logger.debug(f"Received Speed event: speed_time_ms_offset={speed_time_ms_offset}")

        return cls(event_type=GameEventType.SPEED, speed_time_ms_offset=speed_time_ms_offset)


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> TrickEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.TRICK:
            raise ValueError(f"Invalid event type: {event_type}")

        trick_id = stream.read_int8()
        trick_score = stream.read_int16()
        trick_xp = CompressedInteger.decompress_from_stream3(stream)

        client.logger.debug(
            f"Received Trick event: trick_id={trick_id}, trick_score={trick_score}, trick_xp={trick_xp}"
        )

        return cls(event_type=GameEventType.TRICK, trick_id=trick_id, trick_score=trick_score, trick_xp=trick_xp)


@dataclass
class AccoladeEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player earns an accolade.

    Attributes:
        accolades_gained (int): The number of accolades that were gained.
    """

    accolades_gained: int  # 1 byte

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> AccoladeEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.ACCOLADE:
            raise ValueError(f"Invalid event type: {event_type}")

        accolades_gained = stream.read_int8()

        client.logger.debug(f"Received Accolade event: accolades_gained={accolades_gained}")

        return cls(event_type=GameEventType.ACCOLADE, accolades_gained=accolades_gained)


@dataclass
class InvisibleEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player uses the ghost ability.

    Attributes:
        ghost_time_ms_offset (int): The offset in milliseconds when the ghost ability
            expires. This is used to calculate the duration of the ghost ability.
    """

    ghost_time_ms_offset: int  # 2 bytes

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> InvisibleEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.INVIS:
            raise ValueError(f"Invalid event type: {event_type}")

        ghost_time_ms_offset = stream.read_int16()

        client.logger.debug(f"Received Invisible event: ghost_time_ms_offset={ghost_time_ms_offset}")

        return cls(event_type=GameEventType.INVIS, ghost_time_ms_offset=ghost_time_ms_offset)


@dataclass
class KilledByEvent(GameEvent):
    """
    Represents a triggered event that occurs when a player is killed by another
    player.

    Attributes:
        killer_id (int): The ID of the player that killed the player.
    """

    killer_id: int

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> KilledByEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.KILLED_BY:
            raise ValueError(f"Invalid event type: {event_type}")

        killer_id = stream.read_int8()

        client.logger.debug(f"Received KilledBy event: killer_id={killer_id}")

        return cls(event_type=GameEventType.KILLED_BY, killer_id=killer_id)


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> RadiationCloudEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.RADIATION_CLOUD:
            raise ValueError(f"Invalid event type: {event_type}")

        current_map_size = client.game_world.map_size.to_map_size()

        player_id = stream.read_int8()
        x_pos = CompressedFloat.from_stream(current_map_size, stream).value
        y_pos = CompressedFloat.from_stream(current_map_size, stream).value
        time_remaining = CompressedFloat.from_stream(16.0, stream).value

        client.logger.debug(
            f"Received RadiationCloud event: player_id={player_id}, x_pos={x_pos}, y_pos={y_pos}, "
            f"time_remaining={time_remaining}"
        )

        return cls(
            event_type=GameEventType.RADIATION_CLOUD,
            player_id=player_id,
            x_pos=x_pos,
            y_pos=y_pos,
            time_remaining=time_remaining,
        )


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> ChargeEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.CHARGE:
            raise ValueError(f"Invalid event type: {event_type}")

        player_id = stream.read_int8()
        charge_type = ChargeType(stream.read_int8())

        client.logger.debug(f"Received Charge event: player_id={player_id}, charge_type={charge_type.name}")

        return cls(event_type=GameEventType.CHARGE, player_id=player_id, charge_type=charge_type)


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> LPCountEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.LP_COUNT:
            raise ValueError(f"Invalid event type: {event_type}")

        lp_count = stream.read_int8()

        client.logger.debug(f"Received LPCount event: lp_count={lp_count}")

        return cls(event_type=GameEventType.LP_COUNT, lp_count=lp_count)


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

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> BRBoundsEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.BR_BOUNDS:
            raise ValueError(f"Invalid event type: {event_type}")

        current_map_size = client.game_world.map_size.to_map_size()

        bounds_left = CompressedFloat.from_stream(current_map_size, stream).value
        bounds_top = CompressedFloat.from_stream(current_map_size, stream).value
        bounds_right = CompressedFloat.from_stream(current_map_size, stream).value
        bounds_bottom = CompressedFloat.from_stream(current_map_size, stream).value
        lim_bounds_left = CompressedFloat.from_stream(current_map_size, stream).value
        lim_bounds_top = CompressedFloat.from_stream(current_map_size, stream).value
        lim_bounds_right = CompressedFloat.from_stream(current_map_size, stream).value
        lim_bounds_bottom = CompressedFloat.from_stream(current_map_size, stream).value

        client.logger.debug(
            f"Received BRBounds event: bounds_left={bounds_left}, bounds_top={bounds_top}, "
            f"bounds_right={bounds_right}, bounds_bottom={bounds_bottom}, lim_bounds_left={lim_bounds_left}, "
            f"lim_bounds_top={lim_bounds_top}, lim_bounds_right={lim_bounds_right}, "
            f"lim_bounds_bottom={lim_bounds_bottom}"
        )

        return cls(
            event_type=GameEventType.BR_BOUNDS,
            bounds_left=bounds_left,
            bounds_top=bounds_top,
            bounds_right=bounds_right,
            bounds_bottom=bounds_bottom,
            lim_bounds_left=lim_bounds_left,
            lim_bounds_top=lim_bounds_top,
            lim_bounds_right=lim_bounds_right,
            lim_bounds_bottom=lim_bounds_bottom,
        )


@dataclass
class RLGLStateEvent(GameEvent):
    """
    Represents a triggered event that occurs when the state of the Red Light,
    Green Light game mode is updated. This event is only triggered in the RLGL
    game mode.

    Attributes:
        state (RLGLState): The state of the RLGL game mode.
    """

    state: RLGLState  # 1 byte

    @classmethod
    def read(cls, client: Client, stream: DeserializingStream) -> RLGLStateEvent:
        event_type = stream.read_int8()

        if event_type != GameEventType.RLGL_STATE:
            raise ValueError(f"Invalid event type: {event_type}")

        state = RLGLState(stream.read_int8())

        client.logger.debug(f"Received RLGLState event: state={state.name}")

        return cls(event_type=GameEventType.RLGL_STATE, state=state)


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
    GameEventType.CHARGE: ChargeEvent,
    GameEventType.LP_COUNT: LPCountEvent,
    GameEventType.BR_BOUNDS: BRBoundsEvent,
    GameEventType.MINIMAP: GameEvent,
    GameEventType.RLGL_DEATH: GameEvent,
    GameEventType.RLGL_STATE: RLGLStateEvent,
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
