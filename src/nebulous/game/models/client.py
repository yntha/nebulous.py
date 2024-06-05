from __future__ import annotations

import time
from socket import AF_INET, SOCK_DGRAM, inet_aton, socket
from typing import cast

from javarandom import Random as JavaRNG
from multiprocess import Event, Process, Queue  # type: ignore

from nebulous.game import InternalCallbacks
from nebulous.game.account import Account, ServerRegions
from nebulous.game.enums import ConnectionResult, PacketType
from nebulous.game.models import ClientConfig, ClientState, ServerData
from nebulous.game.natives import CompressedFloat, MUTF8String, VariableLengthArray
from nebulous.game.packets import ConnectRequest3, ConnectResult2, Disconnect, KeepAlive, Packet, PacketHandler


class Client:
    def __init__(
        self,
        ticket: str,
        region: ServerRegions,
        config: ClientConfig | None = None,
        callbacks: ClientCallbacks | None = None,
    ):
        self.account = Account(ticket, region)
        self.server_data = ServerData()

        if config is None:
            self.config = ClientConfig()
        else:
            self.config = config

        self.rng = JavaRNG()
        self.packet_queue = Queue()
        self.stop_event = Event()
        self.event_loop = None
        self.recv_loop = None
        self.state = ClientState.DISCONNECTED

        if callbacks is None:
            self.callbacks = ClientCallbacks()
        else:
            self.callbacks = callbacks

        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.port_seed = self.rng.nextInt(2)
        self.port = self.next_port()

        self.server_data.client_id = self.rng.nextInt()
        self.server_data.client_id2 = self.rng.nextInt()

    def net_send_loop(self):
        try:
            last_heartbeat = time.time()
            heartbeat_interval = 0.5

            while not self.stop_event.is_set():
                if self.packet_queue.empty():
                    if time.time() - last_heartbeat < heartbeat_interval:
                        continue

                    keep_alive_packet = KeepAlive(
                        PacketType.KEEP_ALIVE,
                        self.server_data.public_id,
                        self.server_data.private_id,
                        inet_aton(self.account.region.ip),
                        self.server_data.client_id,
                    )

                    self.socket.send(keep_alive_packet.write(self))
                    InternalCallbacks.on_keep_alive(self, keep_alive_packet)

                    last_heartbeat = time.time()
                else:
                    packet: Packet = self.packet_queue.get()

                    self.socket.send(packet.write(self))
        except KeyboardInterrupt:
            pass

    def connect(self) -> bool:
        self.state = ClientState.CONNECTING

        try:
            self.socket.connect((self.account.region.ip, self.port))
            self.socket.settimeout(10)
            self.socket.setblocking(True)

            connect_request_3_packet = ConnectRequest3(
                PacketType.CONNECT_REQUEST_3,
                self.config.game_mode,
                self.config.game_difficulty,
                self.config.game_id,
                MUTF8String.from_py_string(""),
                self.config.online_mode,
                self.config.mayhem_mode,
                self.config.skin,
                self.config.eject_skin,
                MUTF8String.from_py_string(self.config.alias),
                self.config.custom_skin,
                VariableLengthArray(1, self.config.alias_colors),
                self.config.pet1,
                self.config.blob_color,
                MUTF8String.from_py_string(self.config.pet1_name),
                self.config.hat_type,
                self.config.custom_pet,
                self.config.halo_type,
                self.config.pet2,
                MUTF8String.from_py_string(self.config.pet2_name),
                self.config.custom_pet2,
                self.config.custom_particle,
                self.config.particle_type,
                self.config.alias_font,
                VariableLengthArray(1, self.config.level_colors),
                self.config.alias_anim,
                self.config.skin2,
                CompressedFloat(self.config.skin_interpolation_rate, 60.0),
                self.config.custom_skin2,
                VariableLengthArray(2, list(self.account.secure_bytes)),
            )

            self.socket.send(connect_request_3_packet.write(self))
            InternalCallbacks.on_connect(self, connect_request_3_packet)

            conn_result_handler = cast(ConnectResult2, PacketHandler.get_handler(PacketType.CONNECT_RESULT_2))
            conn_result = conn_result_handler.read(self, PacketType.CONNECT_RESULT_2, self.socket.recv(0x80))

            if conn_result.result != ConnectionResult.SUCCESS:
                return False

            self.game_id = conn_result.game_id
            self.config.split_multiplier = conn_result.split_multiplier
            self.server_data.public_id = conn_result.client_id
            self.server_data.private_id = conn_result.private_id

            return True
        except TimeoutError:
            return False

    def net_recv_loop(self):
        try:
            while not self.stop_event.is_set():
                # recv up to 8192 bytes
                data = self.socket.recv(0x2000)
                handler = PacketHandler.get_handler(PacketType(data[0]))

                if handler is None:
                    continue

                handler.read(self, PacketType(data[0]), data)
        except KeyboardInterrupt:
            pass

    def start(self):
        if self.connect():
            self.state = ClientState.CONNECTED
            self.event_loop = Process(target=self.net_send_loop)
            self.recv_loop = Process(target=self.net_recv_loop)

            self.event_loop.start()
            self.recv_loop.start()
        else:
            self.stop()

            return

    def run_forever(self):
        if self.event_loop is not None and self.recv_loop is not None:
            try:
                self.event_loop.join()
                self.recv_loop.join()
            except KeyboardInterrupt:
                self.stop()

    def stop(self):
        if self.event_loop is None or self.recv_loop is None:
            return

        self.state = ClientState.DISCONNECTING

        self.stop_event.set()
        self.event_loop.terminate()
        self.event_loop.join()
        self.recv_loop.terminate()
        self.recv_loop.join()

        self.event_loop = None
        self.recv_loop = None

        disconnect_packet = Disconnect(
            PacketType.DISCONNECT,
            self.server_data.public_id,
            self.server_data.private_id,
            self.server_data.client_id,
        )

        self.socket.send(disconnect_packet.write(self))
        InternalCallbacks.on_disconnect(self, disconnect_packet)
        self.socket.close()

        self.state = ClientState.DISCONNECTED

    def next_port(self) -> int:
        port = self.port_seed + 27900

        self.port_seed += 1
        self.port_seed %= 2

        return port


class ClientCallbacks:
    def on_connect(self, client: Client, packet: ConnectRequest3) -> ConnectRequest3:
        return packet

    def on_disconnect(self, client: Client, packet: Disconnect) -> Disconnect:
        return packet

    def on_keep_alive(self, client: Client, packet: KeepAlive) -> KeepAlive:
        return packet

    def on_connect_result(self, client: Client, packet: ConnectResult2) -> ConnectResult2:
        return packet
