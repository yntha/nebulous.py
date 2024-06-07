from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from nebulous.game.enums import ClanRole, CustomSkinStatus, Font, ProfileVisibility, Relationship


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
    bio_fonts: list[Font] = field(default_factory=([Font.DEFAULT] * 23).copy)


@dataclass
class APIPlayerGeneralStats:
    xp: int
    dots_eaten: int
    blobs_eaten: int
    blobs_lost: int
    biggest_blob: int
    mass_gained: int
    mass_ejected: int
    eject_count: int
    split_count: int
    average_score: int
    highest_score: int
    times_restarted: int
    longest_life_ms: int
    games_won: int
    smbh_collided_count: int
    smbh_eaten_count: int
    bh_collided_count: int
    arenas_won: int
    clan_wars_won: int
    tbh_collided_count: int
    times_teleported: int
    powerups_used: int
    trick_count: int
    matches_won: int
    challenges_won: int
    years_played: int
    accolades: int
    max_plasma_chain: int
    coins_collected: int
    triangles_destroyed: int
    squares_destroyed: int
    pentagons_destroyed: int
    hexagons_destroyed: int
    players_killed: int
    shots_fired: int
    damage_dealt: int
    damage_taken: int
    damage_healed: int
    achievements_earned: list[int] = field(default_factory=[].copy)
    achievement_stats: list[Any] = field(default_factory=[].copy)  # i havent been able to figure this out yet
    special_objects: list[dict[str, str]] = field(default_factory=[].copy)


@dataclass
class APIPlayerStats:
    account_id: int
    account_name: str
    competition_banned: bool
    competition_banned_until_ms: int
    chat_banned: bool
    chat_banned_until_ms: int
    is_supporter: bool
    dq: int
    dq_done: int
    xp_multiplier: int
    xp_multiplier_s: int
    mass_boost: int
    mass_boost_s: int
    plasma_boost: int
    plasma_boost_s: int
    click_type: int
    click_type_s: int
    length_boost: int
    length_boost_s: int
    purchased_alias_colors: bool
    purchased_clan_colors: bool
    purchased_blob_color: bool
    click_enabled: bool
    xp_boost_enabled: bool
    mass_boost_enabled: bool
    current_coins: int
    purchased_skin_map: bool
    purchased_second_pet: bool
    unlocked_multiskin: bool
    is_apple_guest: bool
    clan: Clan
    clan_member: ClanMember
    general_stats: APIPlayerGeneralStats
    account_colors: list[int] = field(default_factory=[].copy)
    purchased_avatars: list[int] = field(default_factory=[].copy)
    purchased_eject_skins: list[int] = field(default_factory=[].copy)
    purchased_hats: list[int] = field(default_factory=[].copy)
    purchashed_particles: list[int] = field(default_factory=[].copy)
    purchased_halos: list[int] = field(default_factory=[].copy)
    purchased_pets: list[int] = field(default_factory=[].copy)
    valid_custom_skin_ids: list[int] = field(default_factory=[].copy)
    valid_custom_pet_ids: list[int] = field(default_factory=[].copy)
    valid_custom_particle_ids: list[int] = field(default_factory=[].copy)
    clan_colors: list[int] = field(default_factory=[].copy)


@dataclass
class APISkin:
    skin_id: int
    status: CustomSkinStatus
    purchase_count: int


@dataclass
class APISkinIDs:
    coins: int
    clan_coins: int
    purchased_second_pet: bool
    unlocked_multiskin: bool
    skin_map_price: int
    skins: list[APISkin] = field(default_factory=[].copy)


@dataclass
class BanInfo:
    account_banned: bool
    competition_banned: bool
    chat_banned: bool
    arena_banned: bool


@dataclass
class ClanMember:
    clan: Clan
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
