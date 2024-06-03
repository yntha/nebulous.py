import time
from multiprocessing import Event, Process, Queue
from socket import AF_INET, SOCK_DGRAM, socket
from typing import cast

from javarandom import Random as JavaRNG

from nebulous.game.account import Account, ServerRegions
from nebulous.game.enums import PacketType, ConnectionResult
from nebulous.game.models import ClientConfig, ClientState, ServerData
from nebulous.game.natives import CompressedFloat, MUTF8String, VariableLengthArray
from nebulous.game.packets import ConnectRequest3, ConnectResult2, KeepAlive, Packet, PacketHandler


class Client:
    def __init__(self, ticket: str, region: ServerRegions, config: ClientConfig):
        self.account = Account(ticket, region)
        self.server_data = ServerData()
        self.config = config
        self.rng = JavaRNG()
        self.packet_queue = Queue()
        self.stop_event = Event()
        self.event_loop = None
        self.state = ClientState.DISCONNECTED

        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.port_seed = self.rng.nextInt(2)
        self.port = self.next_port()

        self.server_data.client_id = self.rng.nextInt()
        self.server_data.client_id2 = self.rng.nextInt()

    def net_event_loop(self):
        while not self.stop_event.is_set():
            if self.packet_queue.empty():
                keep_alive_packet = KeepAlive(self.server_data)
                self.socket.send(keep_alive_packet.write())

                time.sleep(0.25)

                continue

            packet: Packet = self.packet_queue.get()

            self.socket.send(packet.write())
            self.parsers[packet.packet_type].read(self.socket.recv(0x1000))  # recv up to 4096 bytes

    def connect(self) -> bool:
        self.state = ClientState.CONNECTING

        try:
            self.socket.connect((self.account.region.ip, self.port))
            self.socket.settimeout(10)

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

            conn_result_handler = cast(ConnectResult2, PacketHandler.get_handler(PacketType.CONNECT_RESULT_2))
            conn_result = conn_result_handler.read(PacketType.CONNECT_RESULT_2, self.socket.recv(0x80))

            if conn_result.result != ConnectionResult.SUCCESS:
                return False

            self.game_id = conn_result.game_id
            self.config.split_multiplier = conn_result.split_multiplier
            self.server_data.public_id = conn_result.client_id
            self.server_data.private_id = conn_result.private_id

            return True
        except TimeoutError:
            return False

    def start(self):
        if self.connect():
            self.state = ClientState.CONNECTED
            self.event_loop = Process(target=self.net_event_loop).start()
        else:
            self.state = ClientState.DISCONNECTED

    def stop(self):
        if self.event_loop is None:
            return

        self.state = ClientState.DISCONNECTING

        self.stop_event.set()
        self.event_loop.join()
        self.socket.close()

    def next_port(self) -> int:
        port = self.port_seed + 27900

        self.port_seed += 1
        self.port_seed %= 2

        return port
