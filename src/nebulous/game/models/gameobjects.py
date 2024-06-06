from dataclasses import dataclass, field

from nebulous.game.enums import (
    EjectSkinType,
    Font,
    GameDifficulty,
    GameMode,
    HaloType,
    HatType,
    NameAnimation,
    ParitcleType,
    PetType,
    Skin,
)
from nebulous.game.models import Clan, PlayerName


@dataclass
class GameObject:
    x: float
    y: float


@dataclass
class Pet(GameObject):
    pet_type: PetType
    level: int
    name: str
    custom_skin: int


@dataclass
class Player(GameObject):
    name: PlayerName
    level: int
    account_id: int
    skin: Skin
    skin2: Skin
    halo: HaloType
    hat: HatType
    font: Font
    eject_skin: EjectSkinType
    particle: ParitcleType
    pet: Pet
    pet2: Pet
    custom_skin: int
    custom_skin2: int
    custom_particle: int
    skin_interpolation_rate: float
    blob_color: int
    team_id: int
    clan: Clan
    click_type: int
    level_colors: list[int] = field(default_factory=([0x77] * 5).copy)
