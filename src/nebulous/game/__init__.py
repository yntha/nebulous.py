from __future__ import annotations

from typing import TYPE_CHECKING

from nebulous.game.models import PlayerName
from nebulous.game.models.apiobjects import Clan, ClanMember
from nebulous.game.models.gameobjects import GamePet, GamePlayer

if TYPE_CHECKING:
    from nebulous.game.models.client import Client
    from nebulous.game.packets import (
        ClanChatMessage,
        ConnectRequest3,
        ConnectResult2,
        Disconnect,
        GameChatMessage,
        GameData,
        KeepAlive,
    )


class InternalCallbacks:
    @staticmethod
    def on_connect(client: Client, packet: ConnectRequest3) -> ConnectRequest3:
        return client.callbacks.on_connect(client, packet)

    @staticmethod
    def on_disconnect(client: Client, packet: Disconnect) -> Disconnect:
        return client.callbacks.on_disconnect(client, packet)

    @staticmethod
    def on_keep_alive(client: Client, packet: KeepAlive) -> KeepAlive:
        return client.callbacks.on_keep_alive(client, packet)

    @staticmethod
    def on_connect_result(client: Client, packet: ConnectResult2) -> ConnectResult2:
        return client.callbacks.on_connect_result(client, packet)

    @staticmethod
    def on_game_data(client: Client, packet: GameData) -> GameData:
        for player in packet.player_objects:
            if player.player_name.value == client.random_alias:
                client.logger.info(f"Found self in game data: {player}")

                client.game_player = GamePlayer(
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
                        Clan(
                            player.clan_name.value,
                            player.clan_colors.values
                        ),
                        False, False, False, False,
                        player.clan_role,
                        player.clan_role,
                        False,
                    ),
                    player.click_type,
                    player.level_colors.values,
                )

        return client.callbacks.on_game_data(client, packet)

    @staticmethod
    def on_game_chat_message(client: Client, packet: GameChatMessage) -> GameChatMessage:
        client.logger.info(f"Received game chat message: {packet.as_json()}")

        return client.callbacks.on_game_chat_message(client, packet)

    @staticmethod
    def on_clan_chat_message(client: Client, packet: ClanChatMessage) -> ClanChatMessage:
        client.logger.info(f"Received clan chat message: {packet.as_json()}")

        return client.callbacks.on_clan_chat_message(client, packet)
