from __future__ import annotations

import enum
import json
import time
from dataclasses import asdict, dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar, Self

from datastream import ByteOrder, DeserializingStream, SerializingStream
from javarandom import Random as JavaRNG

from nebulous.game import InternalCallbacks
from nebulous.game.constants import APP_VERSION
from nebulous.game.enums import (
    ClanRole,
    ConnectResult,
    Font,
    GameDifficulty,
    GameMode,
    NameAnimation,
    PacketType,
    ProfileVisibility,
    Skin,
    SplitMultiplier,
)
from nebulous.game.models.netobjects import NetGameDot, NetGameItem, NetPlayer, NetPlayerEject
from nebulous.game.natives import CompressedFloat, MUTF8String, VariableLengthArray

if TYPE_CHECKING:
    from nebulous.game.models.client import Client


class PacketEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, enum.Enum):
            return o.name

        return super().default(o)

    def encode(self, o: Any) -> str:
        if isinstance(o, enum.Enum):
            o = o.name

        return super().encode(o)


@dataclass
class Packet:
    packet_type: PacketType

    def write(self, client: Client) -> bytes:
        raise NotImplementedError()

    @classmethod
    def read(cls, client: Client, packet_type: PacketType, data: bytes) -> Self:
        raise NotImplementedError()

    def as_json(self, indent: int = 2) -> str:
        return json.dumps(asdict(self), indent=indent, cls=PacketEncoder)


class PacketHandler:
    handlers: ClassVar[dict] = {}

    @classmethod
    def register_handler(cls, packet_type: PacketType):
        def wrapper(handler):
            cls.handlers[packet_type] = handler
            return handler

        return wrapper

    @classmethod
    def get_handler(cls, packet_type: PacketType) -> type[Packet] | None:
        if packet_type not in cls.handlers:
            return None

        return cls.handlers[packet_type]


@dataclass
@PacketHandler.register_handler(PacketType.CONNECT_RESULT_2)
class ConnectResult2(Packet):
    client_id: int  # 4 bytes
    result: ConnectResult  # 1 byte
    public_id: int  # 4 bytes
    private_id: int  # 4 bytes
    game_id: int  # 4 bytes
    ban_length: int  # 4 bytes
    ad_stuff: float  # 4 bytes
    split_multiplier: SplitMultiplier  # 1 byte

    @classmethod
    def read(cls, client: Client, packet_type: PacketType, data: bytes) -> ConnectResult2:
        stream = DeserializingStream(data, byteorder=ByteOrder.NETWORK_ENDIAN)

        # skip over the packet type byte
        stream.read_int8()

        client_id = stream.read_int32()
        result = ConnectResult(stream.read_int8())
        public_id = stream.read_int32()
        private_id = stream.read_int32()
        game_id = stream.read_int32()
        ban_length = stream.read_int32()
        ad_stuff = stream.read_float()
        split_multiplier = SplitMultiplier.from_net(stream.read_int8())

        stream.close()

        return InternalCallbacks.on_connect_result(
            client,
            cls(
                packet_type,
                client_id,
                result,
                public_id,
                private_id,
                game_id,
                ban_length,
                ad_stuff,
                split_multiplier,
            ),
        )


@dataclass
@PacketHandler.register_handler(PacketType.GAME_DATA)
class GameData(Packet):
    public_id: int  # 4 bytes
    map_size: float  # 4 bytes
    player_count: int  # 1 byte
    eject_count: int  # 1 byte
    dot_id_offset: int  # 2 bytes
    dot_count: int  # 2 bytes
    item_id_offset: int  # 1 byte
    item_count: int  # 1 byte
    player_objects: list[NetPlayer] = field(default_factory=list)
    eject_objects: list[NetPlayerEject] = field(default_factory=list)
    dot_objects: list[NetGameDot] = field(default_factory=list)
    item_objects: list[NetGameItem] = field(default_factory=list)

    @classmethod
    def read(cls, client: Client, packet_type: PacketType, data: bytes) -> GameData:
        stream = DeserializingStream(data, byteorder=ByteOrder.NETWORK_ENDIAN)

        # skip over the packet type byte
        stream.read_int8()

        public_id = stream.read_int32()
        map_size = stream.read_float()
        player_count = stream.read_int8()
        eject_count = stream.read_int8()
        dot_id_offset = stream.read_int16()
        dot_count = stream.read_int16()
        item_id_offset = stream.read_int8()
        item_count = stream.read_int8()

        player_objects = []
        for _ in range(player_count):
            player_id = stream.read_int8()
            skin_id = Skin(stream.read_int16())
            eject_skin_id = stream.read_int8()
            custom_skin_id = stream.read_int32()
            custom_pet_id = stream.read_int32()
            pet_id = stream.read_int8()
            pet_level = stream.read_int16()
            pet_name = MUTF8String.from_stream(stream)
            hat_id = stream.read_int8()
            halo_id = stream.read_int8()
            pet_id2 = stream.read_int8()
            pet_level2 = stream.read_int16()
            pet_name2 = MUTF8String.from_stream(stream)
            custom_pet_id2 = stream.read_int32()
            custom_particle_id = stream.read_int32()
            particle_id = stream.read_int8()
            level_colors = VariableLengthArray.from_stream(1, stream)
            name_animation_id = NameAnimation(stream.read_int8())
            skin_id2 = Skin(stream.read_int16())
            skin_interpolation_rate = CompressedFloat.from_stream(60.0, stream)
            custom_skin_id2 = stream.read_int32()
            blob_color = stream.read_int32()
            team_id = stream.read_int8()
            player_name = MUTF8String.from_stream(stream)
            font_id = Font(stream.read_int8())
            alias_colors = VariableLengthArray.from_stream(1, stream)
            account_id = stream.read_int32()
            player_level = stream.read_int16()
            clan_name = MUTF8String.from_stream(stream)
            clan_colors = VariableLengthArray.from_stream(1, stream)
            clan_role = ClanRole(stream.read_int8())
            click_type = stream.read_int8()

            player_objects.append(
                NetPlayer(
                    player_id,
                    skin_id,
                    eject_skin_id,
                    custom_skin_id,
                    custom_pet_id,
                    pet_id,
                    pet_level,
                    pet_name,
                    hat_id,
                    halo_id,
                    pet_id2,
                    pet_level2,
                    pet_name2,
                    custom_pet_id2,
                    custom_particle_id,
                    particle_id,
                    level_colors,
                    name_animation_id,
                    skin_id2,
                    skin_interpolation_rate,
                    custom_skin_id2,
                    blob_color,
                    team_id,
                    player_name,
                    font_id,
                    alias_colors,
                    account_id,
                    player_level,
                    clan_name,
                    clan_colors,
                    clan_role,
                    click_type,
                )
            )

        eject_objects = []
        for _ in range(eject_count):
            eject_id = stream.read_int8()
            xpos = CompressedFloat.from_3(map_size, stream)
            ypos = CompressedFloat.from_3(map_size, stream)
            mass = CompressedFloat.from_3(500000.0, stream)

            eject_objects.append(NetPlayerEject(eject_id, xpos, ypos, mass))

        dot_objects = []
        for i in range(dot_count):
            dot_id = i + dot_id_offset
            xpos = CompressedFloat.from_3(map_size, stream)
            ypos = CompressedFloat.from_3(map_size, stream)

            dot_objects.append(NetGameDot(dot_id, xpos, ypos))

        item_objects = []
        for i in range(item_count):
            item_id = i + item_id_offset
            item_type = stream.read_int8()
            xpos = CompressedFloat.from_3(map_size, stream)
            ypos = CompressedFloat.from_3(map_size, stream)

            item_objects.append(NetGameItem(item_id, item_type, xpos, ypos))

        stream.close()

        return InternalCallbacks.on_game_data(
            client,
            cls(
                packet_type,
                public_id,
                map_size,
                player_count,
                eject_count,
                dot_id_offset,
                dot_count,
                item_id_offset,
                item_count,
                player_objects,
                eject_objects,
                dot_objects,
                item_objects,
            )
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

        data = stream.bytes()

        stream.close()

        return data


@dataclass
@PacketHandler.register_handler(PacketType.DISCONNECT)
class Disconnect(Packet):
    public_id: int
    private_id: int
    client_id: int

    def write(self, client: Client) -> bytes:  # noqa: ARG002
        stream = SerializingStream(byteorder=ByteOrder.NETWORK_ENDIAN)

        stream.write_int8(self.packet_type)
        stream.write_int32(self.public_id)
        stream.write_int32(self.private_id)
        stream.write_int32(self.client_id)

        data = stream.bytes()

        return data


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
    alias_anim: NameAnimation  # 1 byte
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

        rng_seed = client.rng.nextLong()
        server_rng = JavaRNG(rng_seed)

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
        stream.write_int8(self.alias_anim.value)
        stream.write_int16(self.skin2.value)
        stream.write_int16(self.skin_interpolation_rate.compress())
        stream.write_int32(self.custom_skin2)
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

        stream.close()

        # check that the packet header hasnt been altered by the shuffling
        if packet_bytes[0] != PacketType.CONNECT_REQUEST_3:
            raise ValueError("Packet header has been corrupted")

        if packet_bytes[1:5] != b"\x00\x00\x00\x00":
            raise ValueError("Packet header has been corrupted")

        if packet_bytes[5:13] != rng_seed.to_bytes(8, byteorder="big", signed=True):
            raise ValueError("Packet header has been corrupted")

        return bytes(packet_bytes)
