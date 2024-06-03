import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self

from datastream import ByteOrder, DeserializingStream, SerializingStream
from javarandom import Random as JavaRNG

from nebulous.game.constants import APP_VERSION
from nebulous.game.enums import (
    ConnectionResult,
    Font,
    GameDifficulty,
    GameMode,
    PacketType,
    ProfileVisibility,
    Skin,
    SplitMultiplier,
)
from nebulous.game.natives import CompressedFloat, MUTF8String, VariableLengthArray

if TYPE_CHECKING:
    from nebulous.game.models import Client


@dataclass
class Packet:
    packet_type: PacketType

    def write(self, client: Client) -> bytes:
        raise NotImplementedError()

    @classmethod
    def read(cls, packet_type: PacketType, data: bytes) -> Self:
        raise NotImplementedError()


class PacketHandler:
    handlers: ClassVar[dict] = {}

    @classmethod
    def register_handler(cls, packet_type: PacketType):
        def wrapper(handler):
            cls.handlers[packet_type] = handler
            return handler

        return wrapper

    @classmethod
    def get_handler(cls, packet_type: PacketType) -> type[Packet]:
        return cls.handlers[packet_type]


@dataclass
@PacketHandler.register_handler(PacketType.CONNECT_RESULT_2)
class ConnectResult2(Packet):
    client_id: int  # 4 bytes
    result: ConnectionResult  # 1 byte
    public_id: int  # 4 bytes
    private_id: int  # 4 bytes
    game_id: int  # 4 bytes
    ban_length: int  # 4 bytes
    ad_stuff: float  # 4 bytes
    split_multiplier: SplitMultiplier  # 1 byte

    @classmethod
    def read(cls, packet_type: PacketType, data: bytes) -> Self:
        stream = DeserializingStream(data, byteorder=ByteOrder.NETWORK_ENDIAN)

        client_id = stream.read_int32()
        result = ConnectionResult(stream.read_int8())
        public_id = stream.read_int32()
        private_id = stream.read_int32()
        game_id = stream.read_int32()
        ban_length = stream.read_int32()
        ad_stuff = stream.read_float()
        split_multiplier = SplitMultiplier.from_net(stream.read_int8())

        stream.close()

        return cls(
            packet_type,
            client_id,
            result,
            public_id,
            private_id,
            game_id,
            ban_length,
            ad_stuff,
            split_multiplier,
        )


@dataclass
@PacketHandler.register_handler(PacketType.KEEP_ALIVE)
class KeepAlive(Packet):
    public_id: int  # 4 bytes
    private_id: int  # 4 bytes
    server_ip: bytes  # 4 bytes, see socket.inet_aton
    client_id: int  # 4 bytes

    def write(self, client: Client) -> bytes:  # noqa: ARG002
        stream = SerializingStream(byteorder=ByteOrder.NETWORK_ENDIAN)

        stream.write_int8(self.packet_type)
        stream.write_int32(self.public_id)
        stream.write_int32(self.private_id)

        # by default, java.io.DataOutputStream writes integers in big endian format.
        # for some reason unknown to me, the server expects the region's server ip
        # to be in little endian format, so we must manually encode it as such.
        stream.write(self.server_ip[::-1])

        stream.write_int32(self.client_id)

        return stream.bytes()


@dataclass
@PacketHandler.register_handler(PacketType.CONNECT_REQUEST_3)
class ConnectRequest3(Packet):
    # request_id: int - should always be 0, 4 bytes omitted because it is always 0
    # rng_seed: int - 8 bytes, omitted as it is generated below
    # game_version: int - 2 bytes, omitted as it's set below
    # client_id: int - 4 bytes, omitted because it is generated below
    game_mode: GameMode  # 1 bytes
    game_difficulty: GameDifficulty  # 1 bytes
    game_id: int  # 4 bytes
    ticket: MUTF8String  # MUST BE BLANK
    online_mode: ProfileVisibility  # 1 byte
    mayhem: bool  # 1 byte
    skin1: Skin  # 2 bytes
    eject_skin: int  # 1 byte
    alias: MUTF8String  # variable length, max is 16 bytes iirc
    custom_skin: int  # 4 bytes
    alias_colors: VariableLengthArray  # variable length, length size is 1 byte
    pet_id: int  # 1 byte
    blob_color: int  # 4 bytes
    pet_name: MUTF8String  # variable length
    hat_type: int  # 1 byte
    custom_pet: int  # 4 bytes
    halo_type: int  # 1 byte
    pet_id2: int  # 1 byte
    pet_name2: MUTF8String  # variable length
    custom_pet2: int  # 4 bytes
    custom_particle: int  # 4 bytes
    particle_type: int  # 1 byte
    alias_font: Font  # 1 byte
    level_colors: VariableLengthArray  # variable length, length size is 1 byte
    alias_anim: int  # 1 byte
    skin2: Skin  # 2 bytes
    skin_interpolation_rate: CompressedFloat  # 2 bytes, float encoded as a short
    custom_skin2: int  # 4 bytes
    # timestamp: int - 8 bytes, millis, omitted as it is generated below
    sc_bits: VariableLengthArray  # length size is 2 bytes

    def write(self, client: Client) -> bytes:
        stream = SerializingStream(byteorder=ByteOrder.NETWORK_ENDIAN)

        # write packet type
        stream.write_int8(self.packet_type)

        # a new client id has to be generated for each new connection
        while client.server_data.client_id == 0:
            client.server_data.client_id = client.rng.nextInt()

        # the server is expecting the seed to be the first long of a new JavaRandom instance
        server_rng = JavaRNG(client.server_data.client_id)
        rng_seed = server_rng.nextLong()

        # public id is always 0 for the first packet (CONNECT_REQUEST_3)
        stream.write_int32(0)

        stream.write_int64(rng_seed)
        stream.write_int16(APP_VERSION)
        stream.write_int32(client.server_data.client_id)
        stream.write_int8(self.game_mode.value)
        stream.write_int8(self.game_difficulty.value)
        stream.write_int32(self.game_id)
        stream.write(self.ticket.encode())
        stream.write_int8(self.online_mode.value)
        stream.write_bool(self.mayhem)
        stream.write_int16(self.skin1.value)
        stream.write_int8(self.eject_skin)
        stream.write(self.alias.encode())
        stream.write_int32(self.custom_skin)
        stream.write(self.alias_colors.encode())
        stream.write_int8(self.pet_id)
        stream.write_int32(self.blob_color)
        stream.write(self.pet_name.encode())
        stream.write_int8(self.hat_type)
        stream.write_int32(self.custom_pet)
        stream.write_int8(self.halo_type)
        stream.write_int8(self.pet_id2)
        stream.write(self.pet_name2.encode())
        stream.write_int32(self.custom_pet2)
        stream.write_int32(self.custom_particle)
        stream.write_int8(self.particle_type)
        stream.write_int8(self.alias_font.value)
        stream.write(self.level_colors.encode())
        stream.write_int8(self.alias_anim)
        stream.write_int16(self.skin2.value)
        stream.write_int16(self.skin_interpolation_rate.compress())
        stream.write_int64(int(time.time() * 1000))
        stream.write(self.sc_bits.encode())

        # before returning, some byte shuffling must be done
        packet_bytes = bytearray(stream.bytes())
        indices = []

        for i in range(len(packet_bytes) - 14, 0, -1):
            indices.append((i, server_rng.nextInt(i + 1)))

        for pair in indices:
            x = pair[0] + 13
            a = packet_bytes[x]
            y = pair[1] + 13
            packet_bytes[x] = packet_bytes[y]
            packet_bytes[y] = a

        # check that the packet header hasnt been altered by the shuffling
        if packet_bytes[0] != PacketType.CONNECT_REQUEST_3:
            raise ValueError("Packet header has been corrupted")

        if packet_bytes[1:5] != b"\x00\x00\x00\x00":
            raise ValueError("Packet header has been corrupted")

        if packet_bytes[5:13] != rng_seed.to_bytes(8, byteorder="big"):
            raise ValueError("Packet header has been corrupted")

        return bytes(packet_bytes)
