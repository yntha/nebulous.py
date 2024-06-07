import time

from nebulous.game.account import ServerRegions
from nebulous.game.models.client import Client, ClientCallbacks
from nebulous.game.packets import ConnectRequest3, ConnectResult2, Disconnect, GameData, KeepAlive


class TestCallbacks(ClientCallbacks):
    def on_connect(self, client: Client, packet: ConnectRequest3) -> ConnectRequest3:
        print("Connected to server")
        return packet

    def on_disconnect(self, client: Client, packet: Disconnect) -> Disconnect:
        print("Disconnected from server")
        return packet

    def on_keep_alive(self, client: Client, packet: KeepAlive) -> KeepAlive:
        print("Sending keep alive packet")
        return packet

    def on_connect_result(self, client: Client, packet: ConnectResult2) -> ConnectResult2:
        print(f"Received connection result: {packet.result}")
        return packet

    def on_game_data(self, client: Client, packet: GameData) -> GameData:
        print(f"Received game data: {packet.as_json()}")
        return packet


def test_client():
    client = Client("", ServerRegions.US_EAST, callbacks=TestCallbacks())

    client.start()

    # disconnect after 8 seconds
    time.sleep(8)

    client.stop()
