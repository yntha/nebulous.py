from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from nebulous.game.enums import (
    ClanRole,
    CustomSkinStatus,
    Font,
    GameMode,
    ProfileVisibility,
    PurchasableType,
    Relationship,
    SaleType,
)


@dataclass
class PlayerTitles:
    """
    Represents the titles that a player can have in the game.

    Attributes:
        legend (bool): Indicates if the player has the 'legend' title.
        hero (bool): Indicates if the player has the 'hero' title.
        champion (bool): Indicates if the player has the 'champion' title.
        conqueror (bool): Indicates if the player has the 'conqueror' title.
        tricky (bool): Indicates if the player has the 'tricky' title.
        supporter (bool): Indicates if the player has the 'supporter' title.
        master_tamer (bool): Indicates if the player has the 'master_tamer' title.
        tycoon (bool): Indicates if the player has the 'tycoon' title.
    """
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
    """
    Represents a player's profile in the API.

    Attributes:
        bio (str): The player's biography(about me, description).
        avatar (int): The player's avatar.
        set_name_price (int): The price to set the player's name.
        banned (bool): Indicates if the player is banned.
        chat_banned (bool): Indicates if the player is chat banned.
        arena_banned (bool): Indicates if the player is arena banned.
        relationship (Relationship): The player's relationship status.
        bio_font (Font): The font used for the player's biography.
        has_community_skins (bool): Indicates if the player has community skins.
        has_community_pets (bool): Indicates if the player has community pets.
        has_community_particles (bool): Indicates if the player has community particles.
        profile_visibility (ProfileVisibility): The visibility of the player's profile.
        bg_color_enabled (bool): Indicates if the background color is enabled.
        bg_color (int): The background color.
        plasma (int): The amount of plasma the player has.
        years_played (int): The number of years the player has played.
        titles (PlayerTitles): The titles earned by the player.
        views (int): The number of profile views.
        bio_colors (list[int]): The colors used in the player's biography.
        bio_fonts (list[Font]): The fonts used in the player's biography.
    """
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
    """
    Represents the general statistics of a player in the game.

    Attributes:
        xp (int): The experience points of the player.
        dots_eaten (int): The number of dots eaten by the player.
        blobs_eaten (int): The number of blobs eaten by the player.
        blobs_lost (int): The number of blobs lost by the player.
        biggest_blob (int): The size of the biggest blob owned by the player.
        mass_gained (int): The total mass gained by the player.
        mass_ejected (int): The total mass ejected by the player.
        eject_count (int): The number of times the player has ejected mass.
        split_count (int): The number of times the player has split.
        average_score (int): The average score of the player.
        highest_score (int): The highest score achieved by the player.
        times_restarted (int): The number of times the player has restarted the game.
        longest_life_ms (int): The duration of the player's longest life in milliseconds.
        games_won (int): The number of games won by the player.
        smbh_collided_count (int): The number of times the player has collided with a supermassive black hole.
        smbh_eaten_count (int): The number of supermassive black holes eaten by the player.
        bh_collided_count (int): The number of times the player has collided with a black hole.
        arenas_won (int): The number of arenas won by the player.
        clan_wars_won (int): The number of clan wars won by the player.
        tbh_collided_count (int): The number of times the player has collided with a teleport black hole.
        times_teleported (int): The number of times the player has teleported.
        powerups_used (int): The number of power-ups used by the player.
        trick_count (int): The number of tricks performed by the player.
        matches_won (int): The number of matches won by the player.
        challenges_won (int): The number of challenges won by the player.
        years_played (int): The number of years the player has played the game.
        accolades (int): The number of accolades earned by the player.
        max_plasma_chain (int): The maximum plasma chain achieved by the player.
        coins_collected (int): The number of coins collected by the player.
        triangles_destroyed (int): The number of triangles destroyed by the player.
        squares_destroyed (int): The number of squares destroyed by the player.
        pentagons_destroyed (int): The number of pentagons destroyed by the player.
        hexagons_destroyed (int): The number of hexagons destroyed by the player.
        players_killed (int): The number of players killed by the player.
        shots_fired (int): The number of shots fired by the player.
        damage_dealt (int): The total damage dealt by the player.
        damage_taken (int): The total damage taken by the player.
        damage_healed (int): The total damage healed by the player.
        achievements_earned (list[int]): The list of achievements earned by the player.
        achievement_stats (list[Any]): The list of achievement statistics (yet to be figured out).
        special_objects (list[dict[str, str]]): The list of special objects owned by the player.
    """
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
    """
    Represents the statistics and attributes of a player in the game.

    Attributes:
        account_id (int): The ID of the player's account.
        account_name (str): The name of the player's account.
        competition_banned (bool): Indicates if the player is banned from competitions.
        competition_banned_until_ms (int): The timestamp until which the player is banned from competitions.
        chat_banned (bool): Indicates if the player is banned from chat.
        chat_banned_until_ms (int): The timestamp until which the player is banned from chat.
        is_supporter (bool): Indicates if the player is a supporter.
        dq (int): The number of daily quests.
        dq_done (int): The number of daily quests completed by the player.
        xp_multiplier (int): The XP multiplier of the player.
        xp_multiplier_s (int): The duration of the XP multiplier of the player in seconds.
        mass_boost (int): The mass boost of the player (0, 20, 40).
        mass_boost_s (int): The mass boost duration of the player in seconds.
        plasma_boost (int): The plasma boost of the player.
        plasma_boost_s (int): The plasma boost duration of the player in seconds.
        click_type (int): The click type of the player.
        click_type_s (int): The click type duration of the player in seconds.
        length_boost (int): The length boost of the player.
        length_boost_s (int): The length boost duration of the player in seconds.
        purchased_alias_colors (bool): Indicates if the player has purchased alias colors.
        purchased_clan_colors (bool): Indicates if the player has purchased clan colors.
        purchased_blob_color (bool): Indicates if the player has purchased blob color.
        click_enabled (bool): Indicates if the click boost is enabled for the player.
        xp_boost_enabled (bool): Indicates if XP boost is enabled for the player.
        mass_boost_enabled (bool): Indicates if mass boost is enabled for the player.
        current_coins (int): The current number of coins the player has.
        purchased_skin_map (bool): Indicates if the player has purchased a skin map.
        purchased_second_pet (bool): Indicates if the player has purchased a second pet.
        unlocked_multiskin (bool): Indicates if the player has unlocked multiskin.
        is_apple_guest (bool): Indicates if the player is an Apple guest.
        clan (Clan): The clan the player belongs to.
        clan_member (ClanMember): The clan member information of the player.
        general_stats (APIPlayerGeneralStats): The general statistics of the player.
        account_colors (list[int]): The list of account colors the player has purchased.
        purchased_avatars (list[int]): The list of avatars the player has purchased.
        purchased_eject_skins (list[int]): The list of eject skins the player has purchased.
        purchased_hats (list[int]): The list of hats the player has purchased.
        purchashed_particles (list[int]): The list of particles the player has purchased.
        purchased_halos (list[int]): The list of halos the player has purchased.
        purchased_pets (list[int]): The list of pets the player has purchased.
        valid_custom_skin_ids (list[int]): The list of valid custom skin IDs for the player.
        valid_custom_pet_ids (list[int]): The list of valid custom pet IDs for the player.
        valid_custom_particle_ids (list[int]): The list of valid custom particle IDs for the player.
        clan_colors (list[int]): The list of clan colors.
    """
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
    """
    Represents an API Skin object.

    Attributes:
        skin_id (int): The ID of the skin.
        status (CustomSkinStatus): The status of the skin.
        purchase_count (int): The number of times the skin has been purchased.
    """
    skin_id: int
    status: CustomSkinStatus
    purchase_count: int


@dataclass
class APISkinIDs:
    """
    Represents the skin IDs for a player in the game.

    Attributes:
        coins (int): The number of coins(plasma) the player has.
        clan_coins (int): The number of clan coins(plasma) the player has.
        purchased_second_pet (bool): Indicates whether the player has purchased a second pet.
        unlocked_multiskin (bool): Indicates whether the player has unlocked the multiskin feature.
        skin_map_price (int): The price of the skin map in plasma.
        skins (list[APISkin]): The list of APISkin objects representing the player's skins.
    """
    coins: int
    clan_coins: int
    purchased_second_pet: bool
    unlocked_multiskin: bool
    skin_map_price: int
    skins: list[APISkin] = field(default_factory=[].copy)


@dataclass
class BanInfo:
    """
    Represents information about a player's ban status.

    Attributes:
        account_banned (bool): Indicates if the player is banned from their account.
        competition_banned (bool): Indicates if the player is banned from participating in competitions.
        chat_banned (bool): Indicates if the player is banned from using chat.
        arena_banned (bool): Indicates if the player is banned from accessing the game arena.
    """
    account_banned: bool
    competition_banned: bool
    chat_banned: bool
    arena_banned: bool


@dataclass
class ClanMember:
    """
    Represents a member of a clan.

    Attributes:
        clan (Clan): The clan that the member belongs to.
        can_start_clan_war (bool): Indicates whether the member can start a clan war.
        can_join_clan_war (bool): Indicates whether the member can join a clan war.
        can_upload_clan_skin (bool): Indicates whether the member can upload a clan skin.
        can_set_clan_motd (bool): Indicates whether the member can set the clan's message of the day.
        clan_role (ClanRole): The role of the member within the clan.
        effective_clan_role (ClanRole): The effective role of the member within the clan.
        can_self_promote (bool): Indicates whether the member can promote themselves within the clan.
    """
    clan: Clan
    can_start_clan_war: bool
    can_join_clan_war: bool
    can_upload_clan_skin: bool
    can_set_clan_motd: bool
    clan_role: ClanRole = ClanRole.INVALID
    effective_clan_role: ClanRole = ClanRole.INVALID
    can_self_promote: bool = False

@dataclass
class Clan:
    """
    Represents a clan in the game.

    Attributes:
        name (str): The name of the clan.
        colors (list[int]): The colors associated with the clan.
        id (int): The ID of the clan.
        coins (int): The number of coins(plasma) owned by the clan.
    """

    name: str
    colors: list[int] = field(default_factory=([-1] * 6).copy)
    id: int = 0
    coins: int = -1

    @property
    def members(self) -> list[ClanMember]:  # type: ignore
        pass  # todo


@dataclass
class APISaleInfo:
    """
    Represents information about a sale in the API.

    Attributes:
        expires_utc (str): The UTC timestamp of when the sale expires.
        new_taco (bool): Indicates if there is a new youtube link for Taco's YouTube channel.
        new_discord (bool): Indicates if there is a new discord link.
        announcement_url (str): URL to a game announcement.
        sale_types (list[SaleType]): The types of sales associated with this sale info.
    """
    expires_utc: str
    new_taco: bool
    new_discord: bool
    announcement_url: str
    sale_types: list[SaleType] = field(default_factory=[].copy)


@dataclass
class APISkinURLBase:
    """
    Represents the base URL for skin uploads and other related properties.

    Attributes:
        skin_url_base (str): The base URL for skin uploads.
        upload_size_limit_bytes (int): The maximum size limit for skin uploads in bytes.
        upload_pet_size_limit_bytes (int): The maximum size limit for pet skin uploads in bytes.
        server_ip_overrides (dict[str, str]): A dictionary mapping server IPs to their overrides.
        mod_aids (list[int]): A list of moderator AIDs (Account IDs).
        yt_aids (list[int]): A list of YouTube AIDs (Account IDs).
        friend_aids (list[int]): A list of friend AIDs (Account IDs).
        clan_allies (list[int]): A list of clan ally IDs.
        clan_enemies (list[int]): A list of clan enemy IDs.
        free_tourneys (bool): Indicates whether free tournaments are enabled.
        free_arenas (bool): Indicates whether free arenas are enabled.
        tutorial_h_ytid (str): The YouTube ID for the horizontal tutorial video. (?)
        tutorial_v_ytid (str): The YouTube ID for the vertical tutorial video. (?)
        game_mode_ytids (list[str]): A list of YouTube IDs for game modes. (?)
        double_xp_game_mode (GameMode): The game mode granting double XP.
    """
    skin_url_base: str
    upload_size_limit_bytes: int
    upload_pet_size_limit_bytes: int
    server_ip_overrides: dict[str, str]
    mod_aids: list[int]
    yt_aids: list[int]
    friend_aids: list[int]
    clan_allies: list[int]
    clan_enemies: list[int]
    free_tourneys: bool
    free_arenas: bool
    tutorial_h_ytid: str
    tutorial_v_ytid: str
    game_mode_ytids: list[str]
    double_xp_game_mode: GameMode


@dataclass
class APICoinPurchaseResult:
    """
    Represents the result of a coin(plasma) purchase in the API.

    Attributes:
        item_type (PurchasableType): The type of the purchased item.
        item_id (int): The ID of the purchased item.
        coins_spent (int): The number of coins spent for the purchase.
        coins (int): The remaining number of coins(plasma) after the purchase.
        clan_coins (int): The number of clan coins(plasma) after the purchase.
    """
    item_type: PurchasableType
    item_id: int
    coins_spent: int
    coins: int
    clan_coins: int


@dataclass
class APISkinData:
    """
    Represents the data for an API skin.

    Attributes:
        skin_status (CustomSkinStatus): The status of the skin.
        skin_data (bytes): The skin data.
    """
    skin_status: CustomSkinStatus
    skin_data: bytes


@dataclass
class APICheckinResult:
    """
    Represents the result of a check-in operation.

    Attributes:
        checkin_reward (int): The reward for the check-in.
        reward_videos_remaining (int): The number of reward videos remaining.
        coins (int): The number of coins(plasma) after the check-in.
    """
    checkin_reward: int
    reward_videos_remaining: int
    coins: int


@dataclass
class APIAlerts:
    """
    Represents the alerts for a player in the game API.

    Attributes:
        has_friend_requests (bool): Indicates if the player has pending friend requests.
        has_clan_invites (bool): Indicates if the player has pending clan invites.
        coins (int): The number of coins the player has.
        motd (str): The new clan message of the day, if any.
        server_message (str): The broadcasted server message, if any.
        new_mail (bool): Indicates if the player has new mail.
        brand_new_mail (bool): Indicates if the player has brand new mail.
        server_mail (bool): Indicates if the player has server mail.
        birthday (int): The player's birthday.
        birthday_plasma (int): The player's birthday plasma.
        mass_boost (int): The mass boost value.
        mass_boost_s (int): The mass boost duration in seconds.
        ban_reason (str): The reason for the player's ban.
        ban_until_utc (str): The UTC timestamp until which the player is banned.
        competition_ban_reason (str): The reason for the player's competition ban.
        competition_ban_until_utc (str): The UTC timestamp until which the player is competition banned.
        chat_ban_reason (str): The reason for the player's chat ban.
        chat_ban_until_utc (str): The UTC timestamp until which the player is chat banned.
        mass_boost_enabled (bool): Indicates if the mass boost is enabled for the player.
        clan_member (ClanMember): The clan member object associated with the player.
    """
    has_friend_requests: bool
    has_clan_invites: bool
    coins: int
    motd: str
    server_message: str
    new_mail: bool
    brand_new_mail: bool
    server_mail: bool
    birthday: int
    birthday_plasma: int
    mass_boost: int
    mass_boost_s: int
    ban_reason: str
    ban_until_utc: str
    competition_ban_reason: str
    competition_ban_until_utc: str
    chat_ban_reason: str
    chat_ban_until_utc: str
    mass_boost_enabled: bool
    clan_member: ClanMember
