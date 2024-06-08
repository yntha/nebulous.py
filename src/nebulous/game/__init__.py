from __future__ import annotations

from typing import TYPE_CHECKING

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
        return client.callbacks.on_game_data(client, packet)

    @staticmethod
    def on_game_chat_message(client: Client, packet: GameChatMessage) -> GameChatMessage:
        client.logger.info(f"Received game chat message: {packet.as_json()}")

        return client.callbacks.on_game_chat_message(client, packet)

    @staticmethod
    def on_clan_chat_message(client: Client, packet: ClanChatMessage) -> ClanChatMessage:
        client.logger.info(f"Received clan chat message: {packet.as_json()}")

        return client.callbacks.on_clan_chat_message(client, packet)
