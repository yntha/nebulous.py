from __future__ import annotations

from typing import TYPE_CHECKING

from nebulous.game.enums import GameSize
from nebulous.game.models import PlayerName
from nebulous.game.models.apiobjects import Clan, ClanMember
from nebulous.game.models.gameobjects import GameDot, GameItem, GamePet, GamePlayer, GamePlayerMass

if TYPE_CHECKING:
    from nebulous.game.models.client import Client
    from nebulous.game.packets import (
        ClanChatMessage,
        ConnectRequest3,
        ConnectResult2,
        Control,
        Disconnect,
        GameChatMessage,
        GameData,
        KeepAlive,
    )
    from nebulous.game.models.gameevents import (
        GameEvent,
        BlobExplodeEvent,
        EjectEvent,
        SplitEvent,
        RecombineEvent,
        AchievementEarnedEvent,
        XPSetEvent,
        DQSetEvent,
        DQCompletedEvent,
        DQProgressEvent,
        EatSOEvent,
        SetSOEvent,
        LevelUpEvent,
        ArenaRankAchievedEvent,
        BlobStatusEvent,
        TeleportEvent,
        ShootEvent,
        ClanWarWonEvent,
        PlasmaRewardEvent,
        EmoteEvent,
        EndMissionEvent,
        XPGained2Event,
        EatCakeEvent,
        CoinCountEvent,
        SpeedEvent,
        TrickEvent,
        AccoladeEvent,
        InvisibleEvent,
        KilledByEvent,
        RadiationCloudEvent,
        ChargeEvent,
        LPCountEvent,
        BRBoundsEvent,
        RLGLStateEvent,
    )


class InternalCallbacks:
    @staticmethod
    async def on_connect(client: Client, packet: ConnectRequest3) -> ConnectRequest3:
        return await client.callbacks.on_connect(client, packet)

    @staticmethod
    async def on_disconnect(client: Client, packet: Disconnect) -> Disconnect:
        return await client.callbacks.on_disconnect(client, packet)

    @staticmethod
    async def on_keep_alive(client: Client, packet: KeepAlive) -> KeepAlive:
        return await client.callbacks.on_keep_alive(client, packet)

    @staticmethod
    async def on_connect_result(client: Client, packet: ConnectResult2) -> ConnectResult2:
        return await client.callbacks.on_connect_result(client, packet)

    @staticmethod
    async def on_game_data(client: Client, packet: GameData) -> GameData:
        for player in packet.player_objects:
            game_player = GamePlayer(
                0.0,
                0.0,
                PlayerName(
                    player.player_name.value,
                    player.font_id,
                    player.alias_colors.values,
                    player.name_animation_id,
                ),
                player.player_level,
                player.account_id,
                player.player_id,
                player.skin_id,
                player.skin_id2,
                player.halo_id,
                player.hat_id,
                player.eject_skin_id,
                player.particle_id,
                GamePet(
                    0.0,
                    0.0,
                    player.pet_id,
                    player.pet_level,
                    player.pet_name.value,
                    player.custom_pet_id,
                ),
                GamePet(
                    0.0,
                    0.0,
                    player.pet_id2,
                    player.pet_level2,
                    player.pet_name2.value,
                    player.custom_pet_id2,
                ),
                player.custom_skin_id,
                player.custom_skin_id2,
                player.custom_particle_id,
                player.skin_interpolation_rate.value,
                player.blob_color,
                player.team_id,
                ClanMember(
                    Clan(player.clan_name.value, player.clan_colors.values),
                    False,
                    False,
                    False,
                    False,
                    player.clan_role,
                    player.clan_role,
                    False,
                ),
                player.click_type,
                player.level_colors.values,
            )

            if player.player_name.value == client.random_alias:
                client.logger.info(f"Found self in game data: {player}")

                client.game_player = await InternalCallbacks.on_player_ready(client, game_player)  # type: ignore

            client.game_world.players.append(game_player)

        for dot in packet.dot_objects:
            game_dot = GameDot(
                dot.xpos.value,
                dot.ypos.value,
                dot.dot_id,
            )

            client.game_world.dots.append(game_dot)

        for eject in packet.eject_objects:
            game_eject = GamePlayerMass(
                eject.xpos.value,
                eject.ypos.value,
                eject.eject_id,
                eject.mass.value,
            )

            client.game_world.ejects.append(game_eject)

        for item in packet.item_objects:
            game_item = GameItem(
                item.xpos.value,
                item.ypos.value,
                item.item_id,
                item.item_type,
            )

            client.game_world.items.append(game_item)

        client.game_world.map_size = GameSize.from_map_size(packet.map_size)

        return await client.callbacks.on_game_data(client, packet)

    @staticmethod
    async def on_game_chat_message(client: Client, packet: GameChatMessage) -> GameChatMessage:
        client.logger.info(f"Received game chat message: {packet.as_json()}")

        return await client.callbacks.on_game_chat_message(client, packet)

    @staticmethod
    async def on_clan_chat_message(client: Client, packet: ClanChatMessage) -> ClanChatMessage:
        client.logger.info(f"Received clan chat message: {packet.as_json()}")

        return await client.callbacks.on_clan_chat_message(client, packet)

    @staticmethod
    async def on_control(client: Client, packet: Control) -> Control:
        return await client.callbacks.on_control(client, packet)

    @staticmethod
    async def on_player_ready(client: Client, player: GamePlayer) -> GamePlayer:
        return await client.callbacks.on_player_ready(client, player)

    @staticmethod
    async def on_game_event(client: Client, event: GameEvent) -> GameEvent:
        return await client.callbacks.on_game_event(client, event)

    @staticmethod
    async def on_blob_explode_event(client: Client, event: BlobExplodeEvent) -> BlobExplodeEvent:
        return await client.callbacks.on_blob_explode_event(client, event)

    @staticmethod
    async def on_eject_event(client: Client, event: EjectEvent) -> EjectEvent:
        return await client.callbacks.on_eject_event(client, event)

    @staticmethod
    async def on_split_event(client: Client, event: SplitEvent) -> SplitEvent:
        return await client.callbacks.on_split_event(client, event)

    @staticmethod
    async def on_recombine_event(client: Client, event: RecombineEvent) -> RecombineEvent:
        return await client.callbacks.on_recombine_event(client, event)

    @staticmethod
    async def on_achievement_earned_event(client: Client, event: AchievementEarnedEvent) -> AchievementEarnedEvent:
        return await client.callbacks.on_achievement_earned_event(client, event)

    @staticmethod
    async def on_xp_set_event(client: Client, event: XPSetEvent) -> XPSetEvent:
        return await client.callbacks.on_xp_set_event(client, event)

    @staticmethod
    async def on_dq_set_event(client: Client, event: DQSetEvent) -> DQSetEvent:
        return await client.callbacks.on_dq_set_event(client, event)

    @staticmethod
    async def on_dq_completed_event(client: Client, event: DQCompletedEvent) -> DQCompletedEvent:
        return await client.callbacks.on_dq_completed_event(client, event)

    @staticmethod
    async def on_dq_progress_event(client: Client, event: DQProgressEvent) -> DQProgressEvent:
        return await client.callbacks.on_dq_progress_event(client, event)

    @staticmethod
    async def on_eat_so_event(client: Client, event: EatSOEvent) -> EatSOEvent:
        return await client.callbacks.on_eat_so_event(client, event)

    @staticmethod
    async def on_set_so_event(client: Client, event: SetSOEvent) -> SetSOEvent:
        return await client.callbacks.on_set_so_event(client, event)

    @staticmethod
    async def on_level_up_event(client: Client, event: LevelUpEvent) -> LevelUpEvent:
        return await client.callbacks.on_level_up_event(client, event)

    @staticmethod
    async def on_arena_rank_achieved_event(client: Client, event: ArenaRankAchievedEvent) -> ArenaRankAchievedEvent:
        return await client.callbacks.on_arena_rank_achieved_event(client, event)

    @staticmethod
    async def on_blob_status_event(client: Client, event: BlobStatusEvent) -> BlobStatusEvent:
        return await client.callbacks.on_blob_status_event(client, event)

    @staticmethod
    async def on_teleport_event(client: Client, event: TeleportEvent) -> TeleportEvent:
        return await client.callbacks.on_teleport_event(client, event)

    @staticmethod
    async def on_shoot_event(client: Client, event: ShootEvent) -> ShootEvent:
        return await client.callbacks.on_shoot_event(client, event)

    @staticmethod
    async def on_clan_war_won_event(client: Client, event: ClanWarWonEvent) -> ClanWarWonEvent:
        return await client.callbacks.on_clan_war_won_event(client, event)

    @staticmethod
    async def on_plasma_reward_event(client: Client, event: PlasmaRewardEvent) -> PlasmaRewardEvent:
        return await client.callbacks.on_plasma_reward_event(client, event)

    @staticmethod
    async def on_emote_event(client: Client, event: EmoteEvent) -> EmoteEvent:
        return await client.callbacks.on_emote_event(client, event)

    @staticmethod
    async def on_end_mission_event(client: Client, event: EndMissionEvent) -> EndMissionEvent:
        return await client.callbacks.on_end_mission_event(client, event)

    @staticmethod
    async def on_xp_gained2_event(client: Client, event: XPGained2Event) -> XPGained2Event:
        return await client.callbacks.on_xp_gained2_event(client, event)

    @staticmethod
    async def on_eat_cake_event(client: Client, event: EatCakeEvent) -> EatCakeEvent:
        return await client.callbacks.on_eat_cake_event(client, event)

    @staticmethod
    async def on_coin_count_event(client: Client, event: CoinCountEvent) -> CoinCountEvent:
        return await client.callbacks.on_coin_count_event(client, event)

    @staticmethod
    async def on_speed_event(client: Client, event: SpeedEvent) -> SpeedEvent:
        return await client.callbacks.on_speed_event(client, event)

    @staticmethod
    async def on_trick_event(client: Client, event: TrickEvent) -> TrickEvent:
        return await client.callbacks.on_trick_event(client, event)

    @staticmethod
    async def on_accolade_event(client: Client, event: AccoladeEvent) -> AccoladeEvent:
        return await client.callbacks.on_accolade_event(client, event)

    @staticmethod
    async def on_invisible_event(client: Client, event: InvisibleEvent) -> InvisibleEvent:
        return await client.callbacks.on_invisible_event(client, event)

    @staticmethod
    async def on_killed_by_event(client: Client, event: KilledByEvent) -> KilledByEvent:
        return await client.callbacks.on_killed_by_event(client, event)

    @staticmethod
    async def on_radiation_cloud_event(client: Client, event: RadiationCloudEvent) -> RadiationCloudEvent:
        return await client.callbacks.on_radiation_cloud_event(client, event)

    @staticmethod
    async def on_charge_event(client: Client, event: ChargeEvent) -> ChargeEvent:
        return await client.callbacks.on_charge_event(client, event)

    @staticmethod
    async def on_lp_count_event(client: Client, event: LPCountEvent) -> LPCountEvent:
        return await client.callbacks.on_lp_count_event(client, event)

    @staticmethod
    async def on_br_bounds_event(client: Client, event: BRBoundsEvent) -> BRBoundsEvent:
        return await client.callbacks.on_br_bounds_event(client, event)

    @staticmethod
    async def on_rlgl_state_event(client: Client, event: RLGLStateEvent) -> RLGLStateEvent:
        return await client.callbacks.on_rlgl_state_event(client, event)


__all__ = [
    "InternalCallbacks",
]
