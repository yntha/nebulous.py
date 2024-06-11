from __future__ import annotations

import asyncio
import logging
import logging.handlers
import os.path
import random
import time
from datetime import datetime, timedelta, timezone
from socket import AF_INET, SOCK_DGRAM, inet_aton, socket
from typing import cast

from javarandom import Random as JavaRNG

from nebulous.game import InternalCallbacks
from nebulous.game.account import Account, ServerRegions
from nebulous.game.enums import ConnectResult, ControlFlags, Font, PacketType
from nebulous.game.exceptions import NotSignedInError
from nebulous.game.models import ClientConfig, ClientState, ServerData
from nebulous.game.models.gameobjects import GamePlayer, GameWorld
from nebulous.game.models.netobjects import NetClanMessage, NetGameMessage
from nebulous.game.natives import CompressedFloat, MUTF8String, VariableLengthArray
from nebulous.game.packets import (
    ClanChatMessage,
    ConnectRequest3,
    ConnectResult2,
    Control,
    Disconnect,
    GameChatMessage,
    GameData,
    KeepAlive,
    Packet,
    PacketHandler,
)


class LobbyChatHandler(logging.handlers.BaseRotatingHandler):
    """
    A custom logging handler for handling chat logs.

    Args:
        encoding (str): The encoding to use for the log file. Defaults to "utf-8".
        chat_size (int): The maximum number of chat messages to store in the log file. Defaults to 1000.

    Attributes:
        current_filename (str): The current log file name.
        size (int): The maximum number of chat messages to store in the log file.
        remaining (int): The number of remaining chat messages that can be stored in the log file.

    Methods:
        get_file_name(): Returns the file name for the log file based on the current timestamp and local timezone.
        emit(record: logging.LogRecord) -> None: Writes the log record to the log file, rotating the file if necessary.
        shouldRollover(record: logging.LogRecord) -> bool: Determines whether the log file should be rotated. Unused.

    """

    def __init__(self, encoding: str = "utf-8", chat_size: int = 1000):
        self.current_filename = self.get_file_name()

        if not os.path.exists(os.path.dirname(self.current_filename)):
            os.makedirs(os.path.dirname(self.current_filename), mode=0o755, exist_ok=True)

        self.size = chat_size
        self.remaining = chat_size

        super().__init__(self.current_filename, mode="w", encoding=encoding)

    def get_file_name(self) -> str:
        """
        Returns the file name for the log file based on the current timestamp and local timezone.

        Returns:
            str: The file name for the log file.

        """
        local_offset_sec = -time.timezone if time.localtime().tm_isdst == 0 else -time.altzone
        offset_hours = local_offset_sec // 3600
        offset_minutes = (local_offset_sec % 3600) // 60

        # get local timezone
        local_timezone = timezone(timedelta(hours=offset_hours, minutes=offset_minutes))
        filename = f"lobby_chat_{datetime.now(local_timezone).strftime('%m-%d-%Y_%I-%M-%S-%p')}.log"

        return os.path.join("logs", "chat", filename)

    def emit(self, record: logging.LogRecord) -> None:
        """
        Writes the log record to the log file, rotating the file if necessary.

        Args:
            record (logging.LogRecord): The log record to be written to the log file.

        Returns:
            None

        """
        if self.remaining == 0:
            new_filename = self.get_file_name()

            self.rotate(self.current_filename, new_filename)
            self.remaining = self.size
            self.current_filename = new_filename
        else:
            self.remaining -= 1

        return super().emit(record)

    # logic is handled in emit()
    def shouldRollover(self, record: logging.LogRecord) -> bool:
        return False


class LobbyChat:
    """
    Represents the lobby chat functionality for a client.

    Args:
        client (Client): The client object associated with the lobby chat.
        log_chat (bool, optional): Whether to log chat messages. Defaults to True.
        log_encoding (str, optional): The encoding to use for logging. Defaults to "utf-8".
        log_size (int, optional): The maximum number of chat messages to log. Defaults to 1000.
    """

    def __init__(self, client: Client, log_chat: bool = True, log_encoding: str = "utf-8", log_size: int = 1000):
        self.client = client
        self.alias = self.client.config.alias
        self.alias_colors = self.client.config.alias_colors
        self.alias_font = self.client.config.alias_font
        self.show_broadcast_bubble = False

        if log_chat:
            self.logger = logging.getLogger("LobbyChat")
            self.logger.setLevel(self.client.log_level)

            log_handler = LobbyChatHandler(encoding=log_encoding, chat_size=log_size)
            log_handler.setFormatter(
                logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", "%m/%d/%Y %I:%M:%S %p")
            )

            self.logger.addHandler(log_handler)
        else:
            self.logger = None

        self.game_messages = []
        self.clan_messages = []

    def set_name(self, alias: str):
        self.alias = alias

    def set_colors(self, colors: list[int]):
        self.alias_colors = colors

    def set_font(self, font: Font):
        self.alias_font = font

    def show_bubble(self, show: bool):
        self.show_broadcast_bubble = show

    async def send_game_message(self, message: str):
        """
        Sends a game message to the server.

        Args:
            message (str): The message to be sent.

        Raises:
            NotSignedInError: If the client is not signed in.

        """
        if self.client.account.account_id < 0:
            raise NotSignedInError("Cannot send game message without being signed in.")

        if self.logger is not None:
            self.logger.info(f"GAME: {self.alias}[{self.client.account.account_id}]: {message}")

        chat_message = GameChatMessage(
            PacketType.GAME_CHAT_MESSAGE,
            MUTF8String.from_py_string(self.alias),
            MUTF8String.from_py_string(message),
            VariableLengthArray(1, self.alias_colors),
            self.show_broadcast_bubble,
            self.alias_font,
        )

        await self.client.packet_queue.put(chat_message)

    async def send_clan_message(self, message: str):
        """
        Sends a clan message to the server.

        Args:
            message (str): The message to be sent.

        Raises:
            NotSignedInError: If the client is not signed in.

        """
        if self.client.account.account_id < 0:
            raise NotSignedInError("Cannot send clan message without being signed in.")

        api_player = self.client.account.player_obj

        if self.logger is not None:
            self.logger.info(
                f"CLAN: <{api_player.stats.clan_member.clan_role}> {self.alias}[{api_player.account_id}]: {message}"  # type: ignore
            )

        chat_message = ClanChatMessage(
            PacketType.CLAN_CHAT_MESSAGE,
            MUTF8String.from_py_string(message),
        )

        await self.client.packet_queue.put(chat_message)

    def add_game_message(self, message: NetGameMessage):
        if self.logger is not None:
            self.logger.info(f"GAME: {message.alias}[{message.player_id}]: {message.message}")

        self.game_messages.append(message)

    def add_clan_message(self, message: NetClanMessage):
        if self.logger is not None:
            self.logger.info(
                f"CLAN: <{message.clan_role.name}> {message.alias}[{message.player_id}]: {message.message}"
            )

        self.clan_messages.append(message)


class Client:
    """
    Represents a client that connects to a Nebulous.io game server.

    Args:
        ticket (str): The ticket used for sign-in authentication.
        region (ServerRegions): The server region to connect to.
        config (ClientConfig | None, optional): The client configuration. Defaults to None.
        callbacks (ClientCallbacks | None, optional): The client callbacks. Defaults to None.
    """

    def __init__(
        self,
        ticket: str,
        region: ServerRegions,
        config: ClientConfig | None = None,
        callbacks: ClientCallbacks | None = None,
    ):
        if config is None:
            self.config = ClientConfig()
        else:
            self.config = config

        self.logger = logging.getLogger("Client")
        self.log_level = self.config.log_level

        log_fn = self.get_file_name()

        os.makedirs(os.path.dirname(log_fn), mode=0o755, exist_ok=True)

        logging.basicConfig(
            format="[%(asctime)s %(name)s] %(levelname)s: %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
            filename=log_fn,
            filemode="w",
            encoding="utf-8",
            level=self.log_level,
        )

        self.logger.info("Logger initialized.")

        self.account = Account(ticket, region)
        self.server_data = ServerData()

        self.logger.info(f"Client configuration: {self.config}")

        self.rng = JavaRNG()
        self.packet_queue = asyncio.Queue()
        self.stop_event = asyncio.Event()
        self.game_data_done = asyncio.Event()
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

        # generate a random alias to connect with.
        # the reason for this is because we need to send our player index in the
        # control packets, and the only times we see our player index is in the
        # packets `GAME_DATA` and `GAME_UPDATE`. upon receiving the `GAME_DATA`
        # with our random alias, we can then grab our player ID, and then be able
        # to send control messages.
        self.random_alias = "".join(map(chr, random.choices(range(0x21, 0x7F), k=16)))  # noqa: S311

        self.control_ticks = 0

        self.chat = LobbyChat(self, self.config.log_chat, self.config.chat_log_encoding, self.config.chat_log_size)
        self.api_player = self.account.player_obj
        self.game_player: GamePlayer | None = None
        self.game_world = GameWorld(
            [],
            [],
            [],
            [],
        )

        self.logger.info(f"Client ID: {self.server_data.client_id}")
        self.logger.info(f"Second client ID: {self.server_data.client_id2}")
        self.logger.info(f"Client initialized to connect to {self.account.region.ip}:{self.port}")

    def get_file_name(self) -> str:
        """
        Get the filename for the log file.

        Returns:
            str: The filename for the log file.
        """
        local_offset_sec = -time.timezone if time.localtime().tm_isdst == 0 else -time.altzone
        offset_hours = local_offset_sec // 3600
        offset_minutes = (local_offset_sec % 3600) // 60

        # get local timezone
        local_timezone = timezone(timedelta(hours=offset_hours, minutes=offset_minutes))
        filename = f"client_{datetime.now(local_timezone).strftime('%m-%d-%Y_%I-%M-%S-%p')}.log"

        return os.path.join("logs", filename)

    async def net_send_loop(self):
        """
        Asynchronous method that handles the sending of packets to the server.

        This method continuously sends packets to the server after the lobby data is ready and the client is not
        in the process of stopping. It sends keep-alive packets to maintain the connection with the server and
        also sends control packets to update the server about the client's connection state (assuming).

        If there are packets in the packet queue, it sends those packets instead of the heartbeat.

        Raises:
            TimeoutError: If the socket times out while sending packets.
        """
        logger = logging.getLogger("SendLoop")
        loop = asyncio.get_event_loop()

        logger.info("Starting send loop...")

        try:
            last_heartbeat = time.time()
            heartbeat_interval = 0.5

            while await self.game_data_done.wait() and not self.stop_event.is_set():
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

                    packet_data = keep_alive_packet.write(self)

                    await asyncio.wait_for(loop.sock_sendall(self.socket, packet_data), timeout=5.0)
                    await InternalCallbacks.on_keep_alive(self, keep_alive_packet)

                    # send control packet alongside keep-alive. perhaps the server needs it
                    # to keep track of the client's connection state?
                    logger.info("Sending heartbeat control packet...")
                    control_packet = Control(
                        PacketType.CONTROL,
                        0.0,
                        0.0,
                        ControlFlags.NONE,
                        self.config.screen.as_aspect_ratio(),
                    )

                    packet_data = control_packet.write(self)

                    await asyncio.wait_for(loop.sock_sendall(self.socket, packet_data), timeout=5.0)
                    await InternalCallbacks.on_control(self, control_packet)

                    last_heartbeat = time.time()
                else:
                    packet: Packet = await self.packet_queue.get()

                    logger.info(f"Sending packet: {packet.packet_type.name}")
                    await asyncio.wait_for(loop.sock_sendall(self.socket, packet.write(self)), timeout=5.0)
        except KeyboardInterrupt:
            logger.info("Send loop interrupted.")
        except TimeoutError:
            logger.fatal("Socket timed out.")
        finally:
            if self.state != ClientState.DISCONNECTING and not self.stop_event.is_set():
                await self.stop()

    async def connect(self) -> bool:
        """
        Connects the client to the server.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        self.state = ClientState.CONNECTING
        loop = asyncio.get_event_loop()

        self.logger.info("Connecting to server...")

        try:
            await asyncio.wait_for(loop.sock_connect(self.socket, (self.account.region.ip, self.port)), timeout=5.0)
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
                MUTF8String.from_py_string(self.random_alias),
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

            await asyncio.wait_for(loop.sock_sendall(self.socket, connect_request_3_packet.write(self)), timeout=5.0)
            await InternalCallbacks.on_connect(self, connect_request_3_packet)

            self.logger.info("Connect request sent. Waiting for connect result...")

            conn_result_handler = cast(ConnectResult2, PacketHandler.get_handler(PacketType.CONNECT_RESULT_2))
            conn_result = await conn_result_handler.read(
                self,
                PacketType.CONNECT_RESULT_2,
                await asyncio.wait_for(loop.sock_recv(self.socket, 0x80), timeout=5.0),
            )

            self.logger.info(f"Connect result received. Result: {conn_result.result.name}")

            if conn_result.result != ConnectResult.SUCCESS:
                return False

            self.game_id = conn_result.game_id
            self.config.split_multiplier = conn_result.split_multiplier
            self.server_data.public_id = conn_result.public_id
            self.server_data.private_id = conn_result.private_id

            self.logger.info(f"Game ID: {self.game_id}")
            self.logger.info(f"Split multiplier: {self.config.split_multiplier}")
            self.logger.info(f"Public ID: {self.server_data.public_id}")
            self.logger.info(f"Private ID: {self.server_data.private_id}")

            return True
        except TimeoutError:
            self.logger.error("[CONNECT] Socket timed out.")

            return False

    async def net_recv_loop(self):
        """
        Asynchronous method that handles the receiving of game server packets.

        This method continuously receives packets from the game server socket and processes them accordingly.
        It checks the packet type, handles initial game data packets, and delegates the packet handling to the
        appropriate handler.

        Raises:
            TimeoutError: If the socket times out.
        """
        # cache value2member map outside of loop
        value2member_map = PacketType._value2member_map_
        logger = logging.getLogger("RecvLoop")
        gamedata_received = 0
        loop = asyncio.get_event_loop()

        logger.info("Starting receive loop...")

        try:
            while not self.stop_event.is_set():
                # recv up to 8192 bytes
                data = await asyncio.wait_for(loop.sock_recv(self.socket, 0x2000), timeout=5.0)

                if data[0] not in value2member_map:
                    logger.error(f"Received unknown packet type: {data[0]}")

                    continue

                packet_handler = PacketHandler.get_handler(PacketType(data[0]))
                packet_name = PacketType(data[0]).name

                if not self.game_data_done.is_set():
                    if packet_name == "GAME_DATA":
                        gamedata_received += 1
                    else:
                        logger.info(
                            f"Received all initial game data packets ({gamedata_received}). Packet sending enabled."
                        )

                        self.game_data_done.set()

                logger.info(f"Received packet: {data.hex()}")

                if packet_handler is None:
                    logger.warn(f"Received unhandled packet type: {packet_name}")

                    continue

                logger.info(f"Received packet: {packet_name}")
                await packet_handler.read(self, PacketType(data[0]), data)
        except KeyboardInterrupt:
            logger.info("Receive loop interrupted.")
        except TimeoutError:
            logger.fatal("Socket timed out.")
        finally:
            if self.state != ClientState.DISCONNECTING and not self.stop_event.is_set():
                await self.stop()

    async def start(self):
        """
        Starts the client and establishes a connection to the server.
        """
        self.logger.info("Starting client...")

        if await self.connect():
            self.state = ClientState.CONNECTED

            self.logger.info("Client connected successfully.")

            self.event_loop = asyncio.create_task(self.net_send_loop())
            self.recv_loop = asyncio.create_task(self.net_recv_loop())

            await asyncio.gather(self.event_loop, self.recv_loop)
        else:
            self.logger.error("Client failed to connect.")
            await self.stop()

            return

    async def stop(self):
        """
        Stops the client and disconnects from the server. Sends a disconnect packet to the server.
        """
        if self.event_loop is None or self.recv_loop is None:
            self.logger.warning("Client is already stopped.")

            return

        self.logger.info("Stopping client...")

        self.state = ClientState.DISCONNECTING
        loop = asyncio.get_event_loop()

        self.stop_event.set()

        self.event_loop = None
        self.recv_loop = None

        self.logger.info("Client stopped. Sending disconnect...")

        disconnect_packet = Disconnect(
            PacketType.DISCONNECT,
            self.server_data.public_id,
            self.server_data.private_id,
            self.server_data.client_id,
        )

        try:
            await asyncio.wait_for(loop.sock_sendall(self.socket, disconnect_packet.write(self)), timeout=5.0)
        except TimeoutError:
            self.logger.error("[STOP] Socket timed out.")

        await InternalCallbacks.on_disconnect(self, disconnect_packet)

        self.logger.info("Disconnect packet sent. Closing socket...")
        self.socket.close()

        self.state = ClientState.DISCONNECTED

    def next_port(self) -> int:
        """
        Generates the next available port number for the client.

        Returns:
            int: The next available port number.
        """
        port = self.port_seed + 27900

        self.port_seed += 1
        self.port_seed %= 2

        return port


class ClientCallbacks:
    async def on_connect(self, client: Client, packet: ConnectRequest3) -> ConnectRequest3:
        """
        Called when the client sends a connect request.

        Args:
            client (Client): The client instance.
            packet (ConnectRequest3): The connect request packet.

        Returns:
            ConnectRequest3: The connect request packet.
        """
        return packet

    async def on_disconnect(self, client: Client, packet: Disconnect) -> Disconnect:
        """
        Called when the client disconnects from the server.

        Args:
            client (Client): The client instance.
            packet (Disconnect): The disconnect packet containing information about the disconnection.

        Returns:
            Disconnect: The disconnect packet.
        """
        return packet

    async def on_keep_alive(self, client: Client, packet: KeepAlive) -> KeepAlive:
        """
        Called when the client sends a keep-alive packet to the server.

        Parameters:
        - client (Client): The client instance.
        - packet (KeepAlive): The KeepAlive packet received from the server.

        Returns:
        - KeepAlive: The KeepAlive packet.
        """
        return packet

    async def on_connect_result(self, client: Client, packet: ConnectResult2) -> ConnectResult2:
        """
        Called when the client receives a connect result packet from the server.

        Args:
            client (Client): The client instance.
            packet (ConnectResult2): The connect result packet.

        Returns:
            ConnectResult2: The connect result packet.
        """
        return packet

    async def on_game_data(self, client: Client, packet: GameData) -> GameData:
        """
        Called when the client receives game data from the server.

        Args:
            client (Client): The client instance.
            packet (GameData): The game data packet received from the server.

        Returns:
            GameData: The game data packet.
        """
        return packet

    async def on_game_chat_message(self, client: Client, packet: GameChatMessage) -> GameChatMessage:
        """
        Called when a game chat message is received.

        Args:
            client (Client): The client instance.
            packet (GameChatMessage): The game chat message packet.

        Returns:
            GameChatMessage: The game chat message packet.
        """
        return packet

    async def on_clan_chat_message(self, client: Client, packet: ClanChatMessage) -> ClanChatMessage:
        """
        Called when a clan chat message is received.

        Args:
            client (Client): The client instance.
            packet (ClanChatMessage): The received clan chat message packet.

        Returns:
            ClanChatMessage: The clan chat message packet.
        """
        return packet

    async def on_control(self, client: Client, packet: Control) -> Control:
        """
        Called when a control packet is received.

        Args:
            client (Client): The client instance.
            packet (Control): The control packet received from/sent by the client.

        Returns:
            Control: The control packet.
        """
        return packet

    async def on_player_ready(self, client: Client, player: GamePlayer) -> GamePlayer:
        """
        Called when a player is ready to interact with the lobby.

        Args:
            client (Client): The client instance.
            player (GamePlayer): The player object representing the player.

        Returns:
            GamePlayer: The player object.
        """
        return player
