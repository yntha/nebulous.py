import time
from multiprocessing import Event, Process, Queue
from socket import AF_INET, SOCK_DGRAM, socket
from socket import timeout as SocketTimeout  # noqa: N812

from javarandom import Random as JavaRNG

from nebulous.game.account import Account, ServerRegions
from nebulous.game.models import ClientConfig, ClientState, ServerData
from nebulous.game.packets import ConnectRequest3, KeepAlive, Packet


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
            )

            self.socket.send(connect_request_3_packet.write())

            conn_result = ConnectResult2.read(self.socket.recv(0x80))

            self.server_data.client_id = conn_result.token1
            self.server_data.cr2_token2 = conn_result.token2

            return True
        except SocketTimeout:
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
