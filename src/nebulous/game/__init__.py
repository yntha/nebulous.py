from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nebulous.game.models.client import Client
    from nebulous.game.packets import ConnectRequest3, ConnectResult2, Disconnect, KeepAlive


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
