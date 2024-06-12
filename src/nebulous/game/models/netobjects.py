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
    """
    Represents a network player in the game. Network players are the player objects returned by
    packets such as GAME_DATA and GAME_UPDATE.

    Attributes:
        player_id (int): The ID of the player (1 byte).
        skin_id (Skin): The ID of the player's skin (2 bytes).
        eject_skin_id (EjectSkinType): The ID of the player's eject skin (1 byte).
        custom_skin_id (int): The ID of the player's custom skin (4 bytes).
        custom_pet_id (int): The ID of the player's custom pet (4 bytes).
        pet_id (PetType): The ID of the player's pet (1 byte).
        pet_level (int): The level of the player's pet (2 bytes).
        pet_name (MUTF8String): The name of the player's pet.
        hat_id (HatType): The ID of the player's hat (1 byte).
        halo_id (HaloType): The ID of the player's halo (1 byte).
        pet_id2 (PetType): The ID of the player's second pet (1 byte).
        pet_level2 (int): The level of the player's second pet (2 bytes).
        pet_name2 (MUTF8String): The name of the player's second pet.
        custom_pet_id2 (int): The ID of the player's second custom pet (4 bytes).
        custom_particle_id (int): The ID of the player's custom particle (4 bytes).
        particle_id (ParitcleType): The ID of the player's particle (1 byte).
        level_colors (VariableLengthArray): The colors associated with the player's level.
        name_animation_id (NameAnimation): The ID of the player's name animation (1 byte).
        skin_id2 (Skin): The ID of the player's second skin (2 bytes).
        skin_interpolation_rate (CompressedFloat): The interpolation rate for the player's skin (2 bytes).
        custom_skin_id2 (int): The ID of the player's second custom skin (4 bytes).
        blob_color (int): The color of the player's blob (4 bytes).
        team_id (int): The ID of the player's team (1 byte).
        player_name (MUTF8String): The name of the player. Max length should be 16.
        font_id (Font): The ID of the player's font (1 byte).
        alias_colors (VariableLengthArray): The colors associated with the player's alias.
        account_id (int): The ID of the player's account (4 bytes).
        player_level (int): The level of the player (2 bytes).
        clan_name (MUTF8String): The name of the player's clan.
        clan_colors (VariableLengthArray): The colors associated with the player's clan.
        clan_role (ClanRole): The role of the player in the clan (1 byte).
        click_type (int): The type of click performed by the player (1 byte).
    """
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
    """
    Represents an ejected mass object in the network game.

    Attributes:
        eject_id (int): The ID of the eject. (1 byte)
        xpos (CompressedFloat): The x-position of the eject, relative to GameData.map_size. (3 bytes)
        ypos (CompressedFloat): The y-position of the eject, relative to GameData.map_size. (3 bytes)
        mass (CompressedFloat): The mass of the eject, relative to 500000.0. (3 bytes)
    """
    eject_id: int  # 1 byte
    xpos: CompressedFloat  # 3 bytes, relative to GameData.map_size
    ypos: CompressedFloat  # 3 bytes, relative to GameData.map_size
    mass: CompressedFloat  # 3 bytes, relative to 500000.0


@dataclass
class NetGameDot:
    """
    Represents a dot in the network game.

    Attributes:
        dot_id (int): The ID of the dot.
        xpos (CompressedFloat): The x-coordinate of the dot, relative to GameData.map_size. (3 bytes)
        ypos (CompressedFloat): The y-coordinate of the dot, relative to GameData.map_size. (3 bytes)
    """
    dot_id: int
    xpos: CompressedFloat  # 3 bytes, relative to GameData.map_size
    ypos: CompressedFloat  # 3 bytes, relative to GameData.map_size


@dataclass
class NetGameItem:
    """
    Represents a network game item.

    Attributes:
        item_id (int): The ID of the item.
        item_type (Item): The type of the item. (1 byte)
        xpos (CompressedFloat): The x-coordinate of the item, relative to GameData.map_size. (3 bytes)
        ypos (CompressedFloat): The y-coordinate of the item, relative to GameData.map_size. (3 bytes)
    """
    item_id: int
    item_type: Item  # 1 byte
    xpos: CompressedFloat  # 3 bytes, relative to GameData.map_size
    ypos: CompressedFloat  # 3 bytes, relative to GameData.map_size


@dataclass
class NetChatMessage:
    """
    Represents a chat message sent by a player over the network.

    Attributes:
        player_id (int): The ID of the player sending the message. (4 bytes)
        alias (MUTF8String): The alias of the player sending the message.
        message (MUTF8String): The content of the chat message.
        alias_colors (VariableLengthArray): The colors associated with the player's alias.
    """
    player_id: int
    alias: MUTF8String
    message: MUTF8String
    alias_colors: VariableLengthArray


@dataclass
class NetGameMessage(NetChatMessage):
    """
    Represents a game chat message sent by a player over the network.

    Attributes:
        alias_font (Font): The font used for the alias. (1 byte)
        show_bauble (bool): Indicates whether to show a bubble over the player's blob. (1 byte)
    """
    alias_font: Font  # 1 byte
    show_bauble: bool  # 1 byte


@dataclass
class NetClanMessage(NetChatMessage):
    """
    Represents a clan chat message sent by a player over the network.

    Attributes:
        clan_role (ClanRole): The role of the clan member who sent the message. (1 byte)
    """
    clan_role: ClanRole  # 1 byte


__all__ = [
    "NetPlayer",
    "NetPlayerEject",
    "NetGameDot",
    "NetGameItem",
    "NetChatMessage",
    "NetGameMessage",
    "NetClanMessage",
]
