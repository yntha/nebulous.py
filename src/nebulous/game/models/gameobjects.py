from dataclasses import dataclass, field

from nebulous.game.enums import (
    EjectSkinType,
    HaloType,
    HatType,
    Item,
    ParitcleType,
    PetType,
    Skin,
)
from nebulous.game.models import PlayerName
from nebulous.game.models.apiobjects import ClanMember


@dataclass
class GameObject:
    """
    Represents a game object.

    Attributes:
        x (float): The x-coordinate of the game object.
        y (float): The y-coordinate of the game object.
    """

    x: float
    y: float


@dataclass
class GamePet(GameObject):
    """
    Represents a pet in the game.

    Attributes:
        pet_type (PetType): The type of the pet.
        level (int): The level of the pet.
        name (str): The name of the pet.
        custom_skin (int): The custom skin ID of the pet.
    """
    pet_type: PetType
    level: int
    name: str
    custom_skin: int


@dataclass
class GamePlayer(GameObject):
    """
    Represents a player in the game.

    Attributes:
        name (PlayerName): The name of the player.
        level (int): The level of the player.
        account_id (int): The account ID of the player.
        index (int): The index of the player.
        skin (Skin): The skin of the player.
        skin2 (Skin): The second skin of the player.
        halo (HaloType): The halo type of the player.
        hat (HatType): The hat type of the player.
        eject_skin (EjectSkinType): The eject skin type of the player.
        particle (ParitcleType): The particle type of the player.
        pet (GamePet): The pet of the player.
        pet2 (GamePet): The second pet of the player.
        custom_skin (int): The custom skin of the player.
        custom_skin2 (int): The second custom skin of the player.
        custom_particle (int): The custom particle of the player.
        skin_interpolation_rate (float): The skin interpolation rate of the player.
        blob_color (int): The blob color of the player.
        team_id (int): The team ID of the player.
        clan_member (ClanMember): The clan member status of the player.
        click_type (int): The click type of the player.
        level_colors (list[int]): The level colors of the player. Default is [0x77] * 5.
    """
    name: PlayerName
    level: int
    account_id: int
    index: int
    skin: Skin
    skin2: Skin
    halo: HaloType
    hat: HatType
    eject_skin: EjectSkinType
    particle: ParitcleType
    pet: GamePet
    pet2: GamePet
    custom_skin: int
    custom_skin2: int
    custom_particle: int
    skin_interpolation_rate: float
    blob_color: int
    team_id: int
    clan_member: ClanMember
    click_type: int
    level_colors: list[int] = field(default_factory=([0x77] * 5).copy)


@dataclass
class GamePlayerMass(GameObject):
    """
    Represents the ejected mass of a player in the game. These are the blobs you see whenever you press the
    shoot button.

    Attributes:
        eject_id (int): The ID of the eject.
        mass (float): The mass of the eject.
    """
    eject_id: int
    mass: float


@dataclass
class GameDot(GameObject):
    """
    Represents a game dot object. A game dot is a dot that can be eaten by players. Each dot gives the player
    1 mass.

    Attributes:
        dot_id (int): The ID of the dot.
    """
    dot_id: int


@dataclass
class GameItem(GameObject):
    """
    Represents a game item in the game. A game item is an item that can be picked up by players (e.g. plasma,
    suns, pumpkins, cakes, etc.).

    Attributes:
        item_id (int): The unique identifier of the item.
        item_type (Item): The type of the item.
    """
    item_id: int
    item_type: Item


@dataclass
class GameWorld:
    """
    Represents the game world containing players, ejects, dots, and items.

    Attributes:
        players (list[GamePlayer]): A list of GamePlayer objects representing the players in the game.
        ejects (list[GamePlayerMass]): A list of GamePlayerMass objects representing the ejected mass in the game.
        dots (list[GameDot]): A list of GameDot objects representing the dots in the game.
        items (list[GameItem]): A list of GameItem objects representing the items in the game.
    """
    players: list[GamePlayer]
    ejects: list[GamePlayerMass]
    dots: list[GameDot]
    items: list[GameItem]


__all__ = [
    "GameObject",
    "GamePet",
    "GamePlayer",
    "GamePlayerMass",
    "GameDot",
    "GameItem",
    "GameWorld",
]
