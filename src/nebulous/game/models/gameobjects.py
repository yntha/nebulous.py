from dataclasses import dataclass, field

from nebulous.game.enums import (
    EjectSkinType,
    HaloType,
    HatType,
    ParitcleType,
    PetType,
    Skin,
)
from nebulous.game.models import PlayerName
from nebulous.game.models.apiobjects import ClanMember


@dataclass
class GameObject:
    x: float
    y: float


@dataclass
class GamePet(GameObject):
    pet_type: PetType
    level: int
    name: str
    custom_skin: int


@dataclass
class GamePlayer(GameObject):
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
