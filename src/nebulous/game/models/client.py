from __future__ import annotations

import logging
import logging.handlers
import time
from socket import AF_INET, SOCK_DGRAM, inet_aton, socket
from typing import cast

from javarandom import Random as JavaRNG
from multiprocess import Event, Process, Queue  # type: ignore

from nebulous.game import InternalCallbacks
from nebulous.game.account import Account, ServerRegions
from nebulous.game.enums import ConnectResult, Font, PacketType
from nebulous.game.models import ClientConfig, ClientState, ServerData
from nebulous.game.natives import CompressedFloat, MUTF8String, VariableLengthArray
from nebulous.game.packets import (
    ConnectRequest3,
    ConnectResult2,
    Disconnect,
    GameChatMessage,
    GameData,
    KeepAlive,
    Packet,
    PacketHandler,
)


class LobbyChat:
    def __init__(self, client: Client):
        self.client = client
        self.alias = self.client.config.alias
        self.alias_colors = self.client.config.alias_colors
        self.alias_font = self.client.config.alias_font
        self.show_broadcast_bubble = False

    def set_name(self, alias: str):
        self.alias = alias

    def set_colors(self, colors: list[int]):
        self.alias_colors = colors

    def set_font(self, font: Font):
        self.alias_font = font

    def show_bubble(self, show: bool):
        self.show_broadcast_bubble = show

    def send_game_message(self, message: str):
        chat_message = GameChatMessage(
            PacketType.GAME_CHAT_MESSAGE,
            MUTF8String.from_py_string(self.alias),
            MUTF8String.from_py_string(message),
            VariableLengthArray(1, self.alias_colors),
            self.show_broadcast_bubble,
            self.alias_font,
        )

        self.client.packet_queue.put(chat_message)


class Client:
    def __init__(
        self,
        ticket: str,
        region: ServerRegions,
        config: ClientConfig | None = None,
        callbacks: ClientCallbacks | None = None,
        log_level: int = logging.INFO,
    ):
        self.logger = logging.getLogger("Client")
        self.log_level = log_level

        logging.basicConfig(
            format="[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
            filename="client.log",
            filemode="w",
            encoding="utf-8",
            level=log_level,
        )

        self.logger.info("Logger initialized.")

        self.account = Account(ticket, region)
        self.server_data = ServerData()

        if config is None:
            self.config = ClientConfig()
        else:
            self.config = config

        self.logger.info(f"Client configuration: {self.config}")

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

        self.chat = LobbyChat(self)

        self.logger.info(f"Client ID: {self.server_data.client_id}")
        self.logger.info(f"Second client ID: {self.server_data.client_id2}")
        self.logger.info(f"Client initialized to connect to {self.account.region.ip}:{self.port}")

    def net_send_loop(self):
        logger = logging.getLogger("SendLoop")
        log_handler = logging.FileHandler("send.log", mode="w", encoding="utf-8")

        logger.addHandler(log_handler)
        logger.setLevel(self.log_level)
        log_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", "%m/%d/%Y %I:%M:%S %p"))
        log_handler.setLevel(self.log_level)

        logger.info("Starting send loop...")

        try:
            last_heartbeat = time.time()
            heartbeat_interval = 0.5

            while not self.stop_event.is_set():
                if self.packet_queue.empty():
                    if time.time() - last_heartbeat < heartbeat_interval:
                        continue

                    logger.info("Sending keep-alive packet...")

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

                    logger.info(f"Sending packet: {packet.packet_type.name}")
                    self.socket.send(packet.write(self))
        except KeyboardInterrupt:
            logger.info("Send loop interrupted.")
            log_handler.close()

    def connect(self) -> bool:
        self.state = ClientState.CONNECTING

        self.logger.info("Connecting to server...")

        try:
            self.socket.connect((self.account.region.ip, self.port))
            self.socket.settimeout(10)
            self.socket.setblocking(True)

            self.logger.info("Socket connected. Sending connect request...")

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

            self.logger.info("Connect request sent. Waiting for connect result...")

            conn_result_handler = cast(ConnectResult2, PacketHandler.get_handler(PacketType.CONNECT_RESULT_2))
            conn_result = conn_result_handler.read(self, PacketType.CONNECT_RESULT_2, self.socket.recv(0x80))

            self.logger.info(f"Connect result received. Result: {conn_result.result.name}")

            if conn_result.result != ConnectResult.SUCCESS:
                return False

            self.game_id = conn_result.game_id
            self.config.split_multiplier = conn_result.split_multiplier
            self.server_data.public_id = conn_result.client_id
            self.server_data.private_id = conn_result.private_id

            self.logger.info(f"Game ID: {self.game_id}")
            self.logger.info(f"Split multiplier: {self.config.split_multiplier}")
            self.logger.info(f"Public ID: {self.server_data.public_id}")
            self.logger.info(f"Private ID: {self.server_data.private_id}")

            return True
        except TimeoutError:
            self.logger.error("Connection timed out.")

            return False

    def net_recv_loop(self):
        # cache value2member map outside of loop
        value2member_map = PacketType._value2member_map_
        logger = logging.getLogger("RecvLoop")
        log_handler = logging.FileHandler("recv.log", mode="w", encoding="utf-8")

        logger.addHandler(log_handler)
        logger.setLevel(self.log_level)
        log_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", "%m/%d/%Y %I:%M:%S %p"))
        log_handler.setLevel(self.log_level)

        logger.info("Starting receive loop...")

        try:
            while not self.stop_event.is_set():
                # recv up to 8192 bytes
                data = self.socket.recv(0x2000)
                if data[0] not in value2member_map:
                    logger.error(f"Received unknown packet type: {data[0]}")

                    continue

                packet_handler = PacketHandler.get_handler(PacketType(data[0]))
                packet_name = PacketType(data[0]).name

                if packet_handler is None:
                    logger.warn(f"Received unhandled packet type: {packet_name}")

                    continue

                logger.info(f"Received packet: {packet_name}")
                packet_handler.read(self, PacketType(data[0]), data)
        except KeyboardInterrupt:
            logger.info("Receive loop interrupted.")
            log_handler.close()

    def start(self):
        self.logger.info("Starting client...")

        if self.connect():
            self.state = ClientState.CONNECTED

            self.logger.info("Client connected successfully.")

            self.event_loop = Process(target=self.net_send_loop)
            self.recv_loop = Process(target=self.net_recv_loop)

            self.event_loop.start()
            self.recv_loop.start()

            self.logger.info("Client started.")
        else:
            self.logger.error("Client failed to connect.")
            self.stop()

            return

    def run_forever(self):
        if self.event_loop is not None and self.recv_loop is not None:
            try:
                self.logger.info("Running client...")
                self.event_loop.join()
                self.recv_loop.join()
            except KeyboardInterrupt:
                self.stop()

    def stop(self):
        if self.event_loop is None or self.recv_loop is None:
            self.logger.warning("Client is already stopped.")

            return

        self.logger.info("Stopping client...")

        self.state = ClientState.DISCONNECTING

        self.stop_event.set()
        self.event_loop.terminate()
        self.event_loop.join()
        self.recv_loop.terminate()
        self.recv_loop.join()

        self.event_loop = None
        self.recv_loop = None

        self.logger.info("Client stopped. Sending disconnect...")

        disconnect_packet = Disconnect(
            PacketType.DISCONNECT,
            self.server_data.public_id,
            self.server_data.private_id,
            self.server_data.client_id,
        )

        self.socket.send(disconnect_packet.write(self))
        InternalCallbacks.on_disconnect(self, disconnect_packet)

        self.logger.info("Disconnect packet sent. Closing socket...")
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

    def on_game_data(self, client: Client, packet: GameData) -> GameData:
        return packet

    def on_game_chat_message(self, client: Client, packet: GameChatMessage) -> GameChatMessage:
        return packet
