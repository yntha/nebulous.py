from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from nebulous.game.enums import ClanRole, Font, ProfileVisibility, Relationship


@dataclass
class PlayerTitles:
    legend: bool
    hero: bool
    champion: bool
    conqueror: bool
    tricky: bool
    supporter: bool
    master_tamer: bool
    tycoon: bool


@dataclass
class APIPlayerProfile:
    bio: str
    avatar: int
    set_name_price: int
    banned: bool
    chat_banned: bool
    arena_banned: bool
    relationship: Relationship
    bio_font: Font
    has_community_skins: bool
    has_community_pets: bool
    has_community_particles: bool
    profile_visibility: ProfileVisibility
    bg_color_enabled: bool
    bg_color: int
    plasma: int
    years_played: int
    titles: PlayerTitles
    views: int
    bio_colors: list[int] = field(default_factory=([0x00] * 23).copy)
    bio_fonts: list[int] = field(default_factory=([0x00] * 23).copy)




@dataclass
class ClanMember:
    can_start_clan_war: bool
    can_join_clan_war: bool
    can_upload_clan_skin: bool
    can_set_clan_motd: bool
    clan_role: ClanRole
    effective_clan_role: ClanRole
    can_self_promote: bool

@dataclass
class Clan:
    name: str
    colors: list[int] = field(default_factory=([-1] * 6).copy)
    id: int = 0
    coins: int = -1

    @property
    def members(self) -> list[ClanMember]:  # type: ignore
        pass  # todo
