from dataclasses import dataclass

from nebulous.game.enums import (
    ClanRole,
    EjectSkinType,
    Font,
    HaloType,
    HatType,
    Item,
    NameAnimation,
    ParitcleType,
    PetType,
    Skin,
)
from nebulous.game.natives import CompressedFloat, MUTF8String, VariableLengthArray


@dataclass
class NetPlayer:
    player_id: int  # 1 byte
    skin_id: Skin  # 2 bytes
    eject_skin_id: EjectSkinType  # 1 byte
    custom_skin_id: int  # 4 bytes
    custom_pet_id: int  # 4 bytes
    pet_id: PetType  # 1 byte
    pet_level: int  # 2 bytes
    pet_name: MUTF8String
    hat_id: HatType  # 1 byte
    halo_id: HaloType  # 1 byte
    pet_id2: PetType  # 1 byte
    pet_level2: int  # 2 bytes
    pet_name2: MUTF8String
    custom_pet_id2: int  # 4 bytes
    custom_particle_id: int  # 4 bytes
    particle_id: ParitcleType  # 1 byte
    level_colors: VariableLengthArray  # length size 1
    name_animation_id: NameAnimation  # 1 byte
    skin_id2: Skin  # 2 bytes
    skin_interpolation_rate: CompressedFloat  # 2 bytes
    custom_skin_id2: int  # 4 bytes
    blob_color: int  # 4 bytes
    team_id: int  # 1 byte
    player_name: MUTF8String
    font_id: Font  # 1 byte
    alias_colors: VariableLengthArray
    account_id: int  # 4 bytes
    player_level: int  # 2 bytes
    clan_name: MUTF8String
    clan_colors: VariableLengthArray
    clan_role: ClanRole  # 1 byte
    click_type: int  # 1 byte


@dataclass
class NetPlayerEject:
    eject_id: int  # 1 byte
    xpos: CompressedFloat  # 3 bytes, relative to GameData.map_size
    ypos: CompressedFloat  # 3 bytes, relative to GameData.map_size
    mass: CompressedFloat  # 3 bytes, relative to 500000.0


@dataclass
class NetGameDot:
    dot_id: int
    xpos: CompressedFloat  # 3 bytes, relative to GameData.map_size
    ypos: CompressedFloat  # 3 bytes, relative to GameData.map_size


@dataclass
class NetGameItem:
    item_id: int
    item_type: Item  # 1 byte
    xpos: CompressedFloat  # 3 bytes, relative to GameData.map_size
    ypos: CompressedFloat  # 3 bytes, relative to GameData.map_size


@dataclass
class NetChatMessage:
    player_id: int
    alias: MUTF8String
    message: MUTF8String
    alias_colors: VariableLengthArray


@dataclass
class NetGameMessage(NetChatMessage):
    alias_font: Font  # 1 byte
    show_bauble: bool  # 1 byte


@dataclass
class NetClanMessage(NetChatMessage):
    clan_role: ClanRole  # 1 byte
