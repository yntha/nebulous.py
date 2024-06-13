import enum


class ConnectResult(enum.Enum):
    """
    Represents the result of a connection attempt to the game servers.

    Attributes:
        SUCCESS (int): The connection attempt was successful.
        GAME_NOT_FOUND (int): The game was not found.
        UNKNOWN (int): An unknown error occurred during the connection attempt.
        ACCOUNT_ALREADY_SIGNED_IN (int): The account is already signed in.
    """
    SUCCESS = 0
    GAME_NOT_FOUND = 1
    UNKNOWN = 2
    ACCOUNT_ALREADY_SIGNED_IN = 3


class JoinResultCode(enum.Enum):
    """
    Enum class representing the result codes for joining a game.

    Attributes:
        SUCCESS (int): Joining the game was successful.
        NAME_TAKEN (int): The name is already taken.
        NAME_INVALID (int): The name is invalid.
        FULL (int): The game is already full.
        GAME_NOT_FOUND (int): The game was not found.
        FRIEND_NOT_FOUND (int): The friend was not found.
        UNKNOWN_ERROR (int): An unknown error occurred.
        DIED_THIS_ROUND (int): The player died in this round.
        CLAN_WAR_NOT_FOUND (int): The clan war was not found.
        CLAN_NOT_FOUND (int): The clan was not found.
        ACCOUNT_NOT_FOUND (int): The account was not found.
        LACK_PERMISSION (int): The player lacks permission.
        REQUEST_TIMED_OUT (int): The request timed out.
        YOU_ARE_SPECTATING (int): The player is spectating.
        PLEASE_WAIT (int): Server has requested the client to wait.
        IS_ARENA (int): The game is an arena.
        ACCOUNT_IN_USE (int): The account is already in use.
        UPDATE_AVAILABLE (int): An update is available.
        INVALID_TOKEN (int): The token is invalid.
        BANNED (int): The player is banned.
        NOT_SIGNED_IN (int): The player is not signed in.
        TOURNAMENTS_DISABLED (int): Tournaments are disabled.
        MUTED (int): The player is muted.
        FRIEND_ALREADY_TEAMED (int): The friend is already teamed.
        GROUP_NOT_FOUND (int): The group was not found.
        COMP_BANNED (int): The player is banned from competitive play.
        QUEUE_POSITION_UPDATE (int): The queue position was updated.
        CHAT_BANNED (int): The player is banned from chat.
        KICKED (int): The player was kicked.
        INCOMPATIBLE_VERSION (int): The game version is incompatible.
    """
    SUCCESS = 0
    NAME_TAKEN = 1
    NAME_INVALID = 2
    FULL = 3
    GAME_NOT_FOUND = 4
    FRIEND_NOT_FOUND = 5
    UNKNOWN_ERROR = 6
    DIED_THIS_ROUND = 7
    CLAN_WAR_NOT_FOUND = 8
    CLAN_NOT_FOUND = 9
    ACCOUNT_NOT_FOUND = 10
    LACK_PERMISSION = 11
    REQUEST_TIMED_OUT = 12
    YOU_ARE_SPECTATING = 13
    PLEASE_WAIT = 14
    IS_ARENA = 15
    ACCOUNT_IN_USE = 16
    UPDATE_AVAILABLE = 17
    INVALID_TOKEN = 18
    BANNED = 19
    NOT_SIGNED_IN = 20
    TOURNAMENTS_DISABLED = 21
    MUTED = 22
    FRIEND_ALREADY_TEAMED = 23
    GROUP_NOT_FOUND = 24
    COMP_BANNED = 25
    QUEUE_POSITION_UPDATE = 26
    CHAT_BANNED = 27
    KICKED = 28
    INCOMPATIBLE_VERSION = 29


class ControlFlags(enum.IntFlag):
    """
    Enum class representing control flags for game actions.

    Attributes:
        NONE (int): No control flag.
        SPLIT (int): Split the primary blob.
        SHOOT (int): Shoot mass out of the primary blob.
        DASH (int): Use the dash ability. Only works in Dash mode.
        GHOST (int): Use the ghost ability. Only works in Ghost mode.
        DISPOSE (int): Dispose of the item held by the primary blob.
        CHARGEUP (int): Charge up the primary blob. Only works in Charge mode.
    """
    NONE = 0x00
    SPLIT = 0x01
    SHOOT = 0x02
    DASH = 0x04
    GHOST = 0x08
    DISPOSE = 0x10
    CHARGEUP = 0x20


class Item(enum.Enum):
    """
    Enum representing the different items in the game.
    """

    PUMPKIN = 0
    SNOWFLAKE = 1
    HEART = 2
    LEAF = 3
    BIGDOT = 4
    COIN = 5
    PRESENT = 6
    BEAD = 7
    EGG = 8
    RAINDROP = 9
    NEBULA = 10
    CANDY = 11
    SUN = 12
    MOON = 13
    NOTE = 14
    CAKE_PLASMA = 15
    CAKE_XP = 16


class SpinType(enum.Enum):
    """
    Enum representing the different types of spin rewards.
    """
    SKIN = 0
    EJECT_SKIN = 1
    HAT = 2
    PET = 3
    PARTICLE = 4
    XP_2X = 5
    XP_3X = 6
    XP_4X = 7
    AUTO = 8
    ULTRA = 9
    PLASMA = 10


class PurchasableType(enum.Enum):
    """
    Enum representing the types of purchasable items in the game.
    """
    BUY_COMMUNITY_SKIN = 0x00
    BUY_COMMUNITY_PET = 0x01
    BUY_COMMUNITY_PARTICLE = 0x02
    XP_2X_1HR = 0x03
    XP_2X_24HR = 0x04
    XP_3X_1HR = 0x05
    XP_3X_24HR = 0x06
    XP_4X_1HR = 0x07
    XP_4X_24HR = 0x08
    XP_5X_1HR = 0x09
    XP_5X_24HR = 0x0A
    MASS_20_1HR = 0x0B
    MASS_20_24HR = 0x0C
    MASS_40_1HR = 0x0D
    MASS_40_24HR = 0x0E
    MASS_20_PERM = 0x0F
    MASS_40_PERM = 0x10
    XP_2X_1D = 0x11
    XP_2X_7D = 0x12
    XP_3X_1D = 0x13
    XP_3X_7D = 0x14
    XP_4X_1D = 0x15
    XP_4X_7D = 0x16
    XP_5X_1D = 0x17
    XP_5X_7D = 0x18
    XP_2X_PERM_CLAN = 0x19
    XP_3X_PERM_CLAN = 0x1A
    XP_4X_PERM_CLAN = 0x1B
    XP_5X_PERM_CLAN = 0x1C
    ORB_XP_2X_1HR = 0x1D
    ORB_XP_2X_24HR = 0x1E
    ORB_XP_2X_PERM = 0x1F
    ORB_XP_3X_1HR = 0x20
    ORB_XP_3X_24HR = 0x21
    ORB_XP_3X_PERM = 0x22
    DERP_XP_2X_1HR = 0x23
    DERP_XP_2X_24HR = 0x24
    DERP_XP_3X_1HR = 0x25
    DERP_XP_3X_24HR = 0x26
    L_5_1HR = 0x27
    L_5_24HR = 0x28
    L_5_PERM = 0x29
    L_10_1HR = 0x2A
    L_10_24HR = 0x2B
    L_10_PERM = 0x2C
    AUTO_1HR = 0x2D
    AUTO_24HR = 0x2E
    ULTRA_1HR = 0x2F
    ULTRA_24HR = 0x30
    SKIN_MAP = 0x31
    ORB_SKIN_MAP = 0x32
    DERP_SKIN_MAP = 0x33
    SKIN_TRIAL = 0x34
    AUTO_PERM = 0x35
    ULTRA_PERM = 0x36
    AUTO_PERM_REFUND = 0x37
    ULTRA_PERM_REFUND = 0x38
    XP_2X_PERM = 0x39
    XP_3X_PERM = 0x3A
    XP_4X_PERM = 0x3B
    XP_5X_PERM = 0x3C
    SECOND_PET = 0x3D
    MULTISKIN = 0x3E
    MULTISKIN_REFUND = 0x3F
    AVATAR = 0x40
    EJECT_SKIN = 0x41
    PET = 0x42
    HAT = 0x43
    CREATE_CLAN = 0x44
    RENAME_CLAN = 0x45
    CLAN_CONTRIBUTION = 0x46
    GIVE_PLASMA = 0x47
    RECEIVE_PLASMA = 0x48
    UPLOADED_ACCOUNT_SKIN = 0x49
    UPLOADED_CLAN_SKIN = 0x4A
    UPLOADED_PET_SKIN = 0x4B
    UPLOADED_CLAN_PET_SKIN = 0x4C
    UPLOADED_ACCOUNT_PARTICLE = 0x4D
    UPLOADED_CLAN_PARTICLE = 0x4E
    WRITE_MAIL = 0x4F
    COLOR_PLAYER_NAME = 0x50
    COLOR_ACCOUNT_NAME = 0x51
    COLOR_PROFILE = 0x52
    COLOR_CLAN_NAME = 0x53
    COLOR_CLAN_DESCRIPTION = 0x54
    COLOR_CLAN_BG = 0x55
    BLOB_COLOR = 0x56
    CLAN_HOUSE_ROOM = 0x57
    PARTICLE = 0x58
    WRITE_MAIL_CLAN = 0x59


class SaleType(enum.Enum):
    """
    Enumeration representing the type of sale.

    Attributes:
        NONE (int): No sale.
        OFFERS (int): Sale through offers.
        IAP (int): Sale through in-app purchases.
        INGAME (int): Sale within the game.
        INGAME_2 (int): Another type of sale within the game.
    """
    NONE = 0
    OFFERS = 1
    IAP = 2
    INGAME = 3
    INGAME_2 = 4


class ChallengeStatus(enum.Enum):
    """
    Enumeration representing the status of a challenge.

    Attributes:
        SENT (int): The challenge has been sent.
        EXPIRED (int): The challenge has expired.
        NOT_FOUND (int): The challenge was not found.
        CHALLENGE_PENDING_FOR_CHALLENGER (int): The challenge is pending for the challenger.
        CHALLENGE_PENDING_FOR_CHALLENGEE (int): The challenge is pending for the challengee.
        DECLINED (int): The challenge has been declined.
        INCOMPATIBLE_VERSION (int): The challenger has an incompatible game version.
    """
    SENT = 0
    EXPIRED = 1
    NOT_FOUND = 2
    CHALLENGE_PENDING_FOR_CHALLENGER = 3
    CHALLENGE_PENDING_FOR_CHALLENGEE = 4
    DECLINED = 5
    INCOMPATIBLE_VERSION = 6


class Relationship(enum.Enum):
    """
    Enumeration representing the relationship status between entities.

    Attributes:
        NONE (int): No relationship exists.
        REQUESTED (int): A relationship has been requested.
        PENDING (int): A relationship is pending.
        MUTUAL (int): A mutual relationship exists.
    """
    NONE = 0
    REQUESTED = 1
    PENDING = 2
    MUTUAL = 3


class CustomSkinType(enum.Enum):
    """
    Enum representing the types of custom skins available in the game.

    Attributes:
        ACCOUNT (int): Represents a custom skin for an account.
        CLAN (int): Represents a custom skin for a clan.
        PET (int): Represents a custom skin for a pet.
        CLAN_PET (int): Represents a custom skin for a clan pet.
        PARTICLE (int): Represents a custom skin for a particle effect.
        CLAN_PARTICLE (int): Represents a custom skin for a clan particle effect.
        ALL (int): Represents a custom skin that applies to all entities.
    """
    ACCOUNT = 0
    CLAN = 1
    PET = 2
    CLAN_PET = 3
    PARTICLE = 4
    CLAN_PARTICLE = 5
    ALL = 6


class CustomSkinStatus(enum.Enum):
    """
    Enum representing the status of a custom skin.

    Attributes:
        UNUSED (int): The custom skin is unused.
        IN_REVIEW (int): The custom skin is in review.
        REFUNDED (int): The custom skin has been refunded.
        REJECTED (int): The custom skin has been rejected.
        APPROVED (int): The custom skin has been approved.
    """
    UNUSED = 0
    IN_REVIEW = 1
    REFUNDED = 2
    REJECTED = 3
    APPROVED = 4


class SkinBundle(enum.Enum):
    HALLOWEEN = 0
    XMAS = 1
    VDAY = 2


class XPMultiplier(enum.Enum):
    """
    Enumeration representing different XP multipliers.

    Attributes:
        XP (int): Represents no XP multiplier.
        XP_DOUBLE (int): Represents a 2x XP multiplier.
        XP_TRIPLE (int): Represents a 3x XP multiplier.
        XP_QUADRUPLE (int): Represents a 4x XP multiplier.
    """
    XP = 0
    XP_DOUBLE = 1
    XP_TRIPLE = 2
    XP_QUADRUPLE = 3


class ReportType(enum.Enum):
    """
    Enum representing different types of reports.

    Attributes:
        HARASSMENT (int): Report type for harassment.
        THREATS (int): Report type for threats.
        SPAM (int): Report type for spam.
        OTHER (int): Report type for other reasons.
        INAPPROPRIATE_SKIN (int): Report type for inappropriate skin.
        MAIL (int): Report type for reporting mail.
        CHAT (int): Report type for reporting chat.
    """
    HARASSMENT = 0
    THREATS = 1
    SPAM = 2
    OTHER = 3
    INAPPROPRIATE_SKIN = 4
    MAIL = 5
    CHAT = 6


class MissionObjective(enum.Enum):
    """
    Enum representing mission objectives.

    Attributes:
        UNKNOWN (int): Unknown mission objective.
        WIN (int): Win the game as the objective.
        KILL_ALL_BOTS (int): Kill all bots as the objective.
        SURVIVE (int): Survive as the objective.
        SCORE (int): Achieve a certain score as the objective.
    """
    UNKNOWN = 0
    WIN = 1
    KILL_ALL_BOTS = 2
    SURVIVE = 3
    SCORE = 4


class ProfileVisibility(enum.Enum):
    """
    Enum representing the visibility options for a user's profile.

    Attributes:
        PUBLIC (int): The profile is visible to everyone.
        CLAN_AND_FRIENDS (int): The profile is visible to the user's clan members and friends.
        FRIENDS (int): The profile is visible to the user's friends only.
    """
    PUBLIC = 0
    CLAN_AND_FRIENDS = 1
    FRIENDS = 2


class ClanRole(enum.Enum):
    """
    Enum representing the roles in a clan.

    Attributes:
        INVALID (int): Invalid role.
        MEMBER (int): Member role.
        ADMIN (int): Admin role.
        LEADER (int): Leader role.
        ELDER (int): Elder role.
        DIAMOND (int): Diamond role.
        INITIATE (int): Initiate role.
    """
    INVALID = 0
    MEMBER = 1
    ADMIN = 2
    LEADER = 3
    ELDER = 4
    DIAMOND = 5
    INITIATE = 6


class HoleType(enum.Enum):
    """
    Enumeration representing different types of blackholes in the game.

    Attributes:
        NORMAL (int): Represents a normal hole.
        SUPERMASSIVE (int): Represents a supermassive hole.
        TELEPORT (int): Represents a teleport hole.
        NEBU (int): Represents a nebula hole.
    """
    NORMAL = 0
    SUPERMASSIVE = 1
    TELEPORT = 2
    NEBU = 3


class SplitMultiplier(enum.Enum):
    """
    Enum class representing split multipliers.

    Attributes:
        X8 (SplitMultiplier): Split multiplier of 8.
        X16 (SplitMultiplier): Split multiplier of 16.
        X32 (SplitMultiplier): Split multiplier of 32.
        X64 (SplitMultiplier): Split multiplier of 64.
    """
    (
        X8,
        X16,
        X32,
        X64,
    ) = range(4)

    @classmethod
    def from_net(cls, value: int) -> "SplitMultiplier":
        """
        Convert a network value to the corresponding SplitMultiplier enum value.

        Args:
            value (int): The network value to convert.

        Returns:
            SplitMultiplier: The corresponding SplitMultiplier enum value.

        Raises:
            ValueError: If the provided value is not a valid SplitMultiplier value.
        """
        match value:
            case 0x08:
                return cls.X8
            case 0x10:
                return cls.X16
            case 0x20:
                return cls.X32
            case 0x40:
                return cls.X64
            case _:
                raise ValueError(f"Invalid SplitMultiplier value: {value}")


class WorldSize(enum.Enum):
    (
        TINY,
        SMALL,
        NORMAL,
        LARGE,
    ) = range(4)


class NameAnimation(enum.Enum):
    NONE = 0
    COLOR_CYCLE_SLOW = 1
    COLOR_CYCLE_FAST = 2
    RAINBOW_HORIZONTAL_SLOW = 3
    RAINBOW_HORIZONTAL_FAST = 4
    RAINBOW_VERTICAL_SLOW = 5
    RAINBOW_VERTICAL_FAST = 6


class Font(enum.Enum):
    DEFAULT = 0
    xxraytid = 1
    xtrusion = 2
    xxon = 3
    xefus = 4
    xenophobia = 5
    xenowort = 6
    cenobyte = 7
    nm_hero = 8
    xmas = 9
    xlines = 10
    xerox_malfunction = 11
    kaushan_script = 12
    great_vibes = 13
    roteflora = 14
    neverwinter = 15
    mh = 16
    kongtext = 17
    sucaba = 18
    ball = 19
    stars = 20
    gettheme = 21
    dephun2 = 22
    theinterzone = 23
    alphaclown = 24
    superhet = 25
    larson = 26
    christmas = 27
    fire = 28
    beyno = 29
    kingthings = 30


class GameDifficulty(enum.Enum):
    (
        EASY,
        MEDIUM,
        HARD,
        IMPOSSIBLE,
    ) = range(4)


import enum

class OnlineStatus(enum.Enum):
    """
    Enumeration representing the online status options for a user.

    Attributes:
        ONLINE(int): The user is online and available.
        APPEAR_OFFLINE(int): The user appears offline to others.
        HIDDEN(int): The user is hidden from others.
        DND(int): The user is in "do not disturb" mode.
    """
    (
        ONLINE,
        APPEAR_OFFLINE,
        HIDDEN,
        DND,
    ) = range(4)


class PacketType(enum.Enum):
    """
    Enumeration representing the different types of packets used in the game.
    """

    INVALID = 0
    """
    Invalid packet type.
    """

    CONNECT_RESULT_2 = 1
    """
    Result of a connection attempt.
    """

    CONTROL = 2
    """
    Control packet.
    """

    KEEP_ALIVE = 3
    """
    Keep-alive packet.
    """

    INVALIDATE_CLIENT = 4
    """
    Invalidate client packet.
    """

    START_GAME_INTERNAL = 5
    """
    Internal packet to start a game.
    """

    CONNECT_REQUEST = 6
    """
    Request to connect to the game server.
    """

    DISCONNECT = 7
    """
    Disconnect packet.
    """

    GAME_CHAT_MESSAGE = 8
    """
    Chat message in the game.
    """

    CLAN_CHAT_MESSAGE = 9
    """
    Chat message in the clan.
    """

    JOIN_REQUEST = 10
    """
    Request to join a game.
    """

    JOIN_RESULT = 11
    """
    Result of a join request.
    """

    TTL_REFRESH_RESPONSE_INTERNAL = 12
    """
    Internal packet for refreshing time-to-live (TTL) response.
    """

    SHUTDOWN_NODE_INTERNAL = 13
    """
    Internal packet to shutdown a node.
    """

    SET_GS_ADDR = 14
    """
    Set game server address packet.
    """

    CLIENT_PREFERENCES = 15
    """
    Client preferences packet.
    """

    SPECTATE_CHANGE = 16
    """
    Spectate change packet.
    """

    CLAN_WAR_LIST_REQUEST = 17
    """
    Request to list clan wars.
    """

    CLAN_WAR_LIST_RESULT = 18
    """
    Result of a clan war list request.
    """

    CLAN_WAR_NOTIFICATION = 19
    """
    Clan war notification packet.
    """

    TOP_SCORES = 20
    """
    Top scores packet.
    """

    SERVER_SHUTDOWN_WARNING = 21
    """
    Server shutdown warning packet.
    """

    GAME_UPDATE = 22
    """
    Game update packet.
    """

    GROUP_LOBBY_LIST_REQUEST = 23
    """
    Request to list group lobbies.
    """

    GROUP_LOBBY_LIST_RESULT = 24
    """
    Result of a group lobby list request.
    """

    PUBLIC_CHAT_MESSAGE = 25
    """
    Public chat message packet.
    """

    ADMIN_INTERNAL = 26
    """
    Internal packet for administrative purposes.
    """

    GROUP_LOBBY_CREATE_REQUEST = 27
    """
    Request to create a group lobby.
    """

    GROUP_LOBBY_CREATE_RESULT = 28
    """
    Result of a group lobby create request.
    """

    GROUP_LOBBY_JOIN_REQUEST = 29
    """
    Request to join a group lobby.
    """

    GROUP_LOBBY_JOIN_RESULT = 30
    """
    Result of a group lobby join request.
    """

    GROUP_LOBBY_UPDATE = 31
    """
    Group lobby update packet.
    """

    GROUP_LOBBY_LEAVE = 32
    """
    Leave group lobby packet.
    """

    ARENA_LIST_REQUEST = 33
    """
    Request to list arenas.
    """

    CLIENT_PREFERENCES_INTERNAL = 34
    """
    Internal packet for client preferences.
    """

    GAME_CRASH_INTERNAL = 35
    """
    Internal packet for game crash.
    """

    PRIVATE_CHAT_MESSAGE = 36
    """
    Private chat message packet.
    """

    ARENA_LEAVE_QUEUE_REQUEST = 37
    """
    Request to leave an arena queue.
    """

    REMOVE_GAME_INTERNAL = 38
    """
    Internal packet to remove a game.
    """

    GROUP_LOBBY_WARN = 39
    """
    Group lobby warning packet.
    """

    ENTER_GAME_REQUEST = 40
    """
    Request to enter a game.
    """

    ENTER_GAME_RESULT = 41
    """
    Result of an enter game request.
    """

    PLAYER_SESSION_STATS_UPDATE_INTERNAL = 42
    """
    Internal packet for updating player session stats.
    """

    PLAYER_WS_ACCOUNT_UPDATE_INTERNAL = 43
    """
    Internal packet for updating player WS account.
    """

    ACCOUNT_STATUS_REQUEST = 44
    """
    Request for account status.
    """

    ACCOUNT_STATUS_RESULT = 45
    """
    Result of an account status request.
    """

    FRIEND_CHAT_MESSAGE = 46
    """
    Chat message from a friend.
    """

    CLIENT_STATUS_CHANGE_REQUEST = 47
    """
    Request to change client status.
    """

    CLIENT_STATUS_CHANGE_RESULT = 48
    """
    Result of a client status change request.
    """

    CLAN_WAR_CONTROL = 49
    """
    Clan war control packet.
    """

    CLAN_WAR_UPDATE = 50
    """
    Clan war update packet.
    """

    ARENA_LIST_RESULT = 51
    """
    Result of an arena list request.
    """

    ADMIN_INTERNAL2 = 52
    """
    Internal packet for administrative purposes.
    """

    NODE_RESET_REQUEST_INTERNAL = 53
    """
    Internal packet for resetting a node.
    """

    CLAN_WAR_RESULT_INTERNAL = 54
    """
    Internal packet for clan war result.
    """

    CLAN_WAR_FORFEIT_INTERNAL = 55
    """
    Internal packet for clan war forfeit.
    """

    SPECTATE_GAME_REQUEST = 56
    """
    Request to spectate a game.
    """

    GET_PLAYER_STATS_INTERNAL = 57
    """
    Internal packet for getting player stats.
    """

    ARENA_QUEUE_REQUEST = 58
    """
    Request to join an arena queue.
    """

    ARENA_STATUS = 59
    """
    Arena status packet.
    """

    ADMIN_INTERNAL3 = 60
    """
    Internal packet for administrative purposes.
    """

    ARENA_RESULT_INTERNAL = 61
    """
    Internal packet for arena result.
    """

    ADMIN_INTERNAL4 = 62
    """
    Internal packet for administrative purposes.
    """

    TEAM_ARENA_RESULT_INTERNAL = 63
    """
    Internal packet for team arena result.
    """

    TEAM_ARENA_STATUS_RESULT = 64
    """
    Result of a team arena status request.
    """

    TEAM_ARENA_STATUS_REQUEST = 65
    """
    Request for team arena status.
    """

    TEAM_ARENA_LIST_REQUEST = 66
    """
    Request to list team arenas.
    """

    TEAM_ARENA_LIST_RESULT = 67
    """
    Result of a team arena list request.
    """

    TEAM_ARENA_QUEUE_REQUEST = 68
    """
    Request to join a team arena queue.
    """

    TEAM_ARENA_LEAVE_QUEUE_REQEUST = 69
    """
    Request to leave a team arena queue.
    """

    TEAM_ARENA_UPDATE = 70
    """
    Team arena update packet.
    """

    CLAN_HOUSE_UPDATE_INTERNAL = 71
    """
    Internal packet for updating clan house.
    """

    ADMIN_INTERNAL5 = 72
    """
    Internal packet for administrative purposes.
    """

    CLAN_HOUSE_UPDATE_INTERNAL2 = 73
    """
    Internal packet for updating clan house.
    """

    NODE_CONNECT_REQUEST_INTERNAL = 74
    """
    Internal packet for connecting a node.
    """

    GAME_DATA = 75
    """
    Game data packet.
    """

    CHALLENGE = 76
    """
    Challenge packet.
    """

    CHALLENGE_RESULT = 77
    """
    Result of a challenge.
    """

    FWD_TO_CLIENT_INTERNAL = 78
    """
    Internal packet for forwarding to client.
    """

    TTL_REFRESH_REQUEST_INTERNAL = 79
    """
    Internal packet for refreshing time-to-live (TTL) request.
    """

    CONNECT_REQUEST_2 = 80
    """
    Second connect request packet.
    """

    CONNECT_RESULT = 81
    """
    Result of a connect request.
    """

    ADMIN_INTERNAL6 = 82
    """
    Internal packet for administrative purposes.
    """

    CLAN_HOUSE_UPDATE_INTERNAL3 = 83
    """
    Internal packet for updating clan house.
    """

    TOURNEY_LIST_REQUEST = 84
    """
    Request to list tournaments.
    """

    TOURNEY_LIST_RESULT = 85
    """
    Result of a tournament list request.
    """

    TOURNEY_ACTION = 86
    """
    Tournament action packet.
    """

    TOURNEY_MATCH_RESULT_INTERNAL = 87
    """
    Internal packet for tournament match result.
    """

    TOURNEY_START_INTERNAL = 88
    """
    Internal packet for starting a tournament.
    """

    TOURNEY_STATUS_UPDATE = 89
    """
    Tournament status update packet.
    """

    ADMIN_INTERNAL7 = 90
    """
    Internal packet for administrative purposes.
    """

    MUTE_INTERNAL = 91
    """
    Internal packet for muting a player.
    """

    JOINED_GAME_INTERNAL = 92
    """
    Internal packet for joining a game.
    """

    CLAN_HOUSE_UPDATE_INTERNAL4 = 93
    """
    Internal packet for updating clan house.
    """

    CLAN_HOUSE_CONFIG = 94
    """
    Clan house configuration packet.
    """

    INVITE = 95
    """
    Invite packet.
    """

    DESIRED_DUO_PARTNER = 96
    """
    Desired duo partner packet.
    """

    EMOTE_REQUEST = 97
    """
    Request to perform an emote.
    """

    UDP_KEEPALIVE = 98
    """
    UDP keep-alive packet.
    """

    GROUP_CHAT_CREATE_REQUEST = 99
    """
    Request to create a group chat.
    """

    GROUP_CHAT_JOIN_REQUEST = 100
    """
    Request to join a group chat.
    """

    GROUP_CHAT_LEAVE_REQUEST = 101
    """
    Request to leave a group chat.
    """

    GROUP_CHAT_RESULT = 102
    """
    Result of a group chat request.
    """

    GROUP_CHAT_STATUS = 103
    """
    Group chat status packet.
    """

    GROUP_CHAT_MESSAGE = 104
    """
    Group chat message packet.
    """

    SESSION_STATS = 105
    """
    Session stats packet.
    """

    ACCOLADE = 106
    """
    Accolade packet.
    """

    VOICE_CONTROL = 107
    """
    Voice control packet.
    """

    VOICE_DATA = 108
    """
    Voice data packet.
    """

    MINIMAP_UPDATE = 109
    """
    Minimap update packet.
    """

    GAME_STOP_INTERNAL = 110
    """
    Internal packet to stop a game.
    """

    BATTLE_ROYALE_ACTION = 111
    """
    Battle Royale action packet.
    """

    BATTLE_ROYALE_LIST_REQUEST = 112
    """
    Request to list Battle Royale games.
    """

    BATTLE_ROYALE_LIST_RESULT = 113
    """
    Result of a Battle Royale list request.
    """

    BATTLE_ROYALE_STATUS_UPDATE = 114
    """
    Battle Royale status update packet.
    """

    BATTLE_ROYALE_RESULT_INTERNAL = 115
    """
    Internal packet for Battle Royale result.
    """

    ADMIN_INTERNAL8 = 116
    """
    Internal packet for administrative purposes.
    """

    PING_MESSAGE = 117
    """
    Ping message packet.
    """

    CONNECT_REQUEST_3 = 118
    """
    Third connect request packet.
    """

    ARENA_CD_INTERNAL = 119
    """
    Internal packet for arena cooldown.
    """


class GameMode(enum.Enum):
    (
        FFA,
        FFA_TIME,
        TEAMS,
        TEAMS_TIME,
        CTF,
        SURVIVAL,
        SOCCER,
        FFA_CLASSIC,
        DOMINATION,
        FFA_ULTRA,
        ZOMBIE_APOCALYPSE,  # NOTE: renamed from "ZA"
        PAINT,
        TEAM_DEATHMATCH,
        X,
        X2,
        X3,
        X4,
        X5,
        SPLIT_16X,
        X6,
        X7,
        CAMPAIGN,
        ROYALEDUO,
        X8,
        TRICK_MODE,  # NOTE: renamed from "X9"
        PLASMA_HUNT,  # NOTE: renamed from "X10"
        X11,
        X12,
        X13,
        X14,
        X15,
        X16,
        X17,
        DASH,  # NOTE: renamed from "X18"
        X19,
        CRAZY_SPLIT,
        INVALID,  # case: Failed to convert gameMode to String
        BATTLE_ROYALE,
        X20,
        X21,
        MEGA_SPLIT,
        CAMPAIGN_2,
        X22,
    ) = range(43)


class Skin(enum.Enum):
    MISC_NONE = 0x00
    MISC_8BALL = 0x01
    MISC_CIRCUIT = 0x02
    MISC_GLOSSYBALL = 0x03
    MISC_LU = 0x04
    MISC_MATRIX = 0x05
    MISC_PAINT = 0x06
    MISC_SOCCER = 0x07
    MISC_WARNING = 0x08
    MISC_YINYANG = 0x09
    MISC_DOGE = 0x0A
    MISC_WAFFLE = 0x0B
    MISC_CLOCK = 0x0C
    MISC_NO_SMOKING = 0x0D
    MISC_PIG = 0x0E
    MISC_TURTLE = 0x0F
    MISC_HELL_DOGE = 0x10
    MISC_POLKADOTS = 0x11
    MISC_POLKADOTS2 = 0x12
    MISC_WHEEL = 0x13
    MISC_COMPASS = 0x14
    MISC_SANIK = 0x15
    MISC_RADIATION = 0x16
    MISC_RADAR = 0x17
    MISC_CREEPER = 0x18
    MISC_BIOHAZARD = 0x19
    MISC_LAMBDA = 0x1A
    MISC_TESLA = 0x1B
    MISC_CHESHIRE = 0x1C
    MISC_JACK = 0x1D
    MISC_COLORS = 0x1E
    MISC_BASEBALL = 0x1F
    MISC_BASKETBALL = 0x20
    MISC_BEACHBALL = 0x21
    MISC_DOOM = 0x22
    MISC_EURO = 0x23
    MISC_EYE = 0x24
    MISC_GRUMPY = 0x25
    MISC_LIGHTNING = 0x26
    MISC_PBALL = 0x27
    MISC_PENNY = 0x28
    MISC_PEPPERMINT = 0x29
    MISC_PINEAPPLE = 0x2A
    MISC_POKER = 0x2B
    MISC_RECORD = 0x2C
    MISC_WHEATLEY = 0x2D
    MISC_CLOUDS = 0x2E
    MISC_CROP = 0x2F
    MISC_SAURON = 0x30
    MISC_SHIP = 0x31
    MISC_WHEEL_CAR = 0x32
    MISC_ZERG = 0x33
    MISC_ROSE = 0x34
    MISC_CD = 0x35
    MISC_CHUTE = 0x36
    MISC_ASTRO = 0x37
    MISC_CHESS = 0x38
    MISC_SIGN = 0x39
    MISC_TROLLFACE = 0x3A
    MISC_MEGUSTAXCF = 0x3B
    MISC_Y = 0x3C
    MISC_DRAGONBALL = 0x3D
    MISC_STAINED = 0x3E
    MISC_STAINED2 = 0x3F
    MISC_BAUBLE = 0x40
    MISC_CAMO = 0x41
    MISC_BULB = 0x42
    MISC_SPIDERWEB = 0x43
    MISC_RAIN = 0x44
    MISC_CHOMP_1 = 0x45
    MISC_SNOW = 0x46
    SCIFI_MERCURY = 0x47
    SCIFI_VENUS = 0x48
    SCIFI_EARTH = 0x49
    SCIFI_MARS = 0x4A
    SCIFI_SATURN = 0x4B
    SCIFI_JUPITER = 0x4C
    SCIFI_NEPTUNE = 0x4D
    SCIFI_MOON = 0x4E
    SCIFI_PLANET1 = 0x4F
    SCIFI_PLANET2 = 0x50
    SCIFI_PLANET3 = 0x51
    SCIFI_PLUTO = 0x52
    SCIFI_SUN = 0x53
    SCIFI_PLANET = 0x54
    SCIFI_DEATHSTAR = 0x55
    SCIFI_PASTRY_CAT = 0x56
    SCIFI_GALAXY = 0x57
    SCIFI_DUST = 0x58
    COUNTRY_AUSTRALIA = 0x59
    COUNTRY_AUSTRIA = 0x5A
    COUNTRY_BELGIUM = 0x5B
    COUNTRY_BRAZIL = 0x5C
    COUNTRY_BULGARIA = 0x5D
    COUNTRY_CANADA = 0x5E
    COUNTRY_CHINA = 0x5F
    COUNTRY_FINLAND = 0x60
    COUNTRY_FRANCE = 0x61
    COUNTRY_GERMANY = 0x62
    COUNTRY_GREECE = 0x63
    COUNTRY_INDIA = 0x64
    COUNTRY_ITALY = 0x65
    COUNTRY_JAPAN = 0x66
    COUNTRY_MEXICO = 0x67
    COUNTRY_NETHERLANDS = 0x68
    COUNTRY_NORWAY = 0x69
    COUNTRY_POLAND = 0x6A
    COUNTRY_ROMANIA = 0x6B
    COUNTRY_RUSSIA = 0x6C
    COUNTRY_SOUTH_AFRICA = 0x6D
    COUNTRY_SOUTHKOREA = 0x6E
    COUNTRY_SPAIN = 0x6F
    COUNTRY_SWEDEN = 0x70
    COUNTRY_TURKEY = 0x71
    COUNTRY_UK = 0x72
    COUNTRY_UKRAINE = 0x73
    COUNTRY_USA = 0x74
    COUNTRY_COLUMBIA = 0x75
    COUNTRY_ECUADOR = 0x76
    COUNTRY_IRELAND = 0x77
    COUNTRY_PUERTO_RICO = 0x78
    COUNTRY_ARGENTINA = 0x79
    COUNTRY_DENMARK = 0x7A
    COUNTRY_EGYPT = 0x7B
    COUNTRY_PERU = 0x7C
    COUNTRY_PORTUGAL = 0x7D
    COUNTRY_GEORGIA = 0x7E
    COUNTRY_MOROCCO = 0x7F
    COUNTRY_CROATIA = 0x80
    COUNTRY_ISRAEL = 0x81
    COUNTRY_PAKISTAN = 0x82
    COUNTRY_BOSNIA = 0x83
    COUNTRY_CHILE = 0x84
    COUNTRY_DR = 0x85
    COUNTRY_HUNGARY = 0x86
    COUNTRY_PHILIPINES = 0x87
    COUNTRY_VENEZUELA = 0x88
    COUNTRY_TRINIDAD = 0x89
    COUNTRY_COSTARICA = 0x8A
    COUNTRY_SCOTLAN = 0x8B
    COUNTRY_BELARUSE = 0x8C
    COUNTRY_SERBIA = 0x8D
    COUNTRY_SLOVAKIA = 0x8E
    COUNTRY_TUNISIA = 0x8F
    COUNTRY_IRAN = 0x90
    COUNTRY_THAILAND = 0x91
    COUNTRY_SWITZERLAND = 0x92
    COUNTRY_ALGERIA = 0x93
    COUNTRY_NEWZEALAND = 0x94
    COUNTRY_LITHUANIA = 0x95
    COUNTRY_JAMAICA = 0x96
    COUNTRY_GUATEMALA = 0x97
    COUNTRY_LEBANON = 0x98
    COUNTRY_ALBANIA = 0x99
    COUNTRY_MACEDONIA = 0x9A
    COUNTRY_LATVIA = 0x9B
    COUNTRY_AZERBAIJAN = 0x9C
    COUNTRY_ESTONIA = 0x9D
    COUNTRY_CZECH = 0x9E
    COUNTRY_WALES = 0x9F
    COUNTRY_ARMENIA = 0xA0
    COUNTRY_CUBA = 0xA1
    COUNTRY_ENGLAND = 0xA2
    COUNTRY_KAZAKHSTAN = 0xA3
    COUNTRY_ICELAND = 0xA4
    COUNTRY_INDONESIA = 0xA5
    COUNTRY_PANAMA = 0xA6
    COUNTRY_CYPRUS = 0xA7
    COUNTRY_MOLDOVA = 0xA8
    COUNTRY_MONTENEGRO = 0xA9
    COUNTRY_HONDURAS = 0xAA
    COUNTRY_ELSALVADOR = 0xAB
    COUNTRY_URUGUAY = 0xAC
    COUNTRY_IRAQ = 0xAD
    COUNTRY_SAUDIAARABIA = 0xAE
    MISC_AWESOME = 0xAF
    MISC_PUG = 0xB0
    MISC_PANDA = 0xB1
    MISC_BIBLETHUMP = 0xB2
    MISC_SAW = 0xB3
    COUNTRY_BOLIVIA = 0xB4
    COUNTRY_JORDAN = 0xB5
    MISC_PENGUIN = 0xB6
    MISC_HEART = 0xB7
    MISC_CIRCUIT_2 = 0xB8
    MISC_COOKIE = 0xB9
    MISC_HOURGLASS = 0xBA
    MISC_MONA = 0xBB
    MISC_POINTER = 0xBC
    MISC_SHIELD = 0xBD
    SCIFI_DUST_BLUE = 0xBE
    SCIFI_DUST_RED = 0xBF
    COUNTRY_BAHRAIN = 0xC0
    MISC_PIZZA = 0xC1
    MISC_BURGER = 0xC2
    MISC_DONUT = 0xC3
    MISC_DRAGON = 0xC4
    MISC_SEAL = 0xC5
    MISC_WOOFER = 0xC6
    MISC_SPIRAL = 0xC7
    MISC_SPIRAL_2 = 0xC8
    MISC_ROUND = 0xC9
    MISC_DEVIL_ALIEN = 0xCA
    MISC_COMET = 0xCB
    MISC_LIGHTNING_BALL = 0xCC
    MISC_FOXY = 0xCD
    SCIFI_PLASMA = 0xCE
    SCIFI_COMET = 0xCF
    MISC_TENNIS = 0xD0
    MISC_ATOM = 0xD1
    MISC_CAT = 0xD2
    MISC_DANDELION = 0xD3
    MISC_LION = 0xD4
    MISC_POTATOCORN = 0xD5
    MISC_OURBOROS = 0xD6
    MISC_DISCOBALL = 0xD7
    SPECIAL_PUMPKIN = 0xD8
    SPECIAL_PUMPKIN_TREE = 0xD9
    SPECIAL_CAT = 0xDA
    SPECIAL_TOWN = 0xDB
    SPECIAL_CEMETARY = 0xDC
    COUNTRY_PARAGUAY = 0xDD
    MISC_BUTTERFLY = 0xDE
    COUNTRY_NICARAGUA = 0xDF
    MISC_BACTERIA = 0xE0
    MISC_DINOSAUR = 0xE1
    MISC_DINOSAUR_2 = 0xE2
    MISC_FIRE_ICE = 0xE3
    MISC_MINION = 0xE4
    ACHIEVE_CW_1 = 0xE5
    MISC_SPIRIT_WOLF = 0xE6
    COUNTRY_QATAR = 0xE7
    COUNTRY_SLOVENIA = 0xE8
    MISC_BOMB = 0xE9
    SCIFI_UNIVERSE = 0xEA
    SCIFI_PRISM_DUST = 0xEB
    COUNTRY_MALAYSIA = 0xEC
    COUNTRY_SYRIA = 0xED
    SCIFI_CALLISTO = 0xEE
    SPECIAL_LEAF = 0xEF
    SPECIAL_ACORN = 0xF0
    SPECIAL_CORNUCOPIA = 0xF1
    SPECIAL_HARVEST = 0xF2
    SPECIAL_AUTUMN_TREE = 0xF3
    MISC_TORUS = 0xF4
    MISC_ORANGE = 0xF5
    MISC_STATIC = 0xF6
    MISC_BURIDOG = 0xF7
    SCIFI_VORTEX = 0xF8
    SCIFI_LINE_SINK = 0xF9
    COUNTRY_KUWAIT = 0xFA
    MISC_WHIRLPOOL = 0xFB
    SCIFI_PLASMA_2 = 0xFC
    SCIFI_PINK_HOLE = 0xFD
    MISC_TURBINE = 0xFE
    SCIFI_HAPPY_STARS = 0xFF
    MISC_MAGMA = 0x100
    MISC_MATRIX_2 = 0x101
    ACHIEVE_ARENA_10 = 0x102
    ACHIEVE_ARENA_100 = 0x103
    ACHIEVE_ARENA_1000 = 0x104
    ACHIEVE_CW_10 = 0x105
    ACHIEVE_CW_100 = 0x106
    PLASMA_CIRCLES = 0x107
    PLASMA_F1TOPDOWN = 0x108
    PLASMA_FACE_1 = 0x109
    PLASMA_FACE_2 = 0x10A
    PLASMA_FACE_3 = 0x10B
    PLASMA_FACE_4 = 0x10C
    PLASMA_FACE_5 = 0x10D
    PLASMA_FACE_6 = 0x10E
    PLASMA_FACE_7 = 0x10F
    PLASMA_FACE_8 = 0x110
    PLASMA_FACE_9 = 0x111
    PLASMA_HAPPY_STARS = 0x112
    PLASMA_PEACOCK = 0x113
    PLASMA_PLANE = 0x114
    MISC_PLASMA_BALL = 0x115
    PLASMA_REEL = 0x116
    PLASMA_SPACE = 0x117
    PLASMA_PURPLEPLANETSTARS = 0x118
    PLASMA_PULSAR = 0x119
    PLASMA_BULB_1 = 0x11A
    PLASMA_BULB_2 = 0x11B
    PLASMA_BULB_3 = 0x11C
    PLASMA_BULB_4 = 0x11D
    PLASMA_BULB_5 = 0x11E
    PLASMA_BULB_6 = 0x11F
    PLASMA_BULB_7 = 0x120
    PLASMA_BULB_8 = 0x121
    PLASMA_BULB_9 = 0x122
    PLASMA_WORMHOLE = 0x123
    PLASMA_COIN = 0x124
    SPECIAL_CHRISTMAS_TREE = 0x125
    SPECIAL_CHRISTMAS_WREATH = 0x126
    SPECIAL_SANTA = 0x127
    SPECIAL_SNOW_GLOBE = 0x128
    SPECIAL_SNOW = 0x129
    SPECIAL_GIFTS = 0x12A
    PLASMA_CLOUDS = 0x12B
    PLASMA_ZOOM = 0x12C
    PLASMA_CLOCK = 0x12D
    MISC_BEACH = 0x12E
    MISC_HAMSTER = 0x12F
    PLASMA_GLOWSTARS = 0x130
    PLASMA_METAL = 0x131
    PLASMA_NEURONS = 0x132
    PLASMA_SHUTTLE = 0x133
    PLASMA_SPACE_2 = 0x134
    SPECIAL_ICE = 0x135
    SPECIAL_ICEBERG = 0x136
    SPECIAL_ICICLES = 0x137
    SPECIAL_IGLOO = 0x138
    SPECIAL_PENGUIN = 0x139
    SPECIAL_SNOWLEAF = 0x13A
    SPECIAL_WINTER_TREE = 0x13B
    MISC_FISH = 0x13C
    PLASMA_BOUNCING_BALL = 0x13D
    MISC_FIREBALL = 0x13E
    CARTOON_SNAIL = 0x13F
    CARTOON_ZEBRA = 0x140
    CARTOON_HIPPO = 0x141
    CARTOON_ELEPHANT = 0x142
    CARTOON_COW = 0x143
    CARTOON_GOAT = 0x144
    CARTOON_BEAR = 0x145
    CARTOON_MOUSE = 0x146
    CARTOON_KANGAROO = 0x147
    CARTOON_DOG = 0x148
    CARTOON_OWL = 0x149
    CARTOON_CAT = 0x14A
    CARTOON_BEAVER = 0x14B
    CARTOON_SHEEP_2 = 0x14C
    CARTOON_PENGUIN = 0x14D
    CARTOON_SHEEP = 0x14E
    COUNTRY_UAE = 0x14F
    LEVEL_EARTH = 0x150
    MISC_CHECKERS = 0x151
    COUNTRY_YEMEN = 0x152
    LEVEL_PHOENIX_FIRE = 0x153
    LEVEL_PHOENIX_ELECTRIC = 0x154
    LEVEL_TAPESTRY = 0x155
    LEVEL_SCALES = 0x156
    SPECIAL_MASKS = 0x157
    SPECIAL_MASK_1 = 0x158
    SPECIAL_MASK_2 = 0x159
    SPECIAL_FEATHERS = 0x15A
    SPECIAL_MASK_3 = 0x15B
    SPECIAL_EASTER_GARDEN = 0x15C
    SPECIAL_EGG_BASKET = 0x15D
    SPECIAL_EASTER_BUNNY = 0x15E
    SPECIAL_EGGS = 0x15F
    SPECIAL_EGGS_TRANSPARENT = 0x160
    SPECIAL_FLOWERS = 0x161
    SPECIAL_CANOPY = 0x162
    SPECIAL_GRASS = 0x163
    SPECIAL_LADYBUG = 0x164
    SPECIAL_BUTTERFLY = 0x165
    LEVEL_ASTEROIDS = 0x166
    LEVEL_DOTTY = 0x167
    LEVEL_LEOPARD = 0x168
    LEVEL_FIRE_WINGS = 0x169
    PLASMA_TESSELATION = 0x16A
    PLASMA_EARTH = 0x16B
    PLASMA_FIREWORK = 0x16C
    PLASMA_BRAIN = 0x16D
    SPECIAL_DESERT_PLANET = 0x16E
    SPECIAL_SPACE_CAT = 0x16F
    SPECIAL_SATELLITE = 0x170
    SPECIAL_STARFIELD = 0x171
    SPECIAL_GALAXY = 0x172
    LEVEL_DRAGON = 0x173
    LEVEL_BH = 0x174
    PLASMA_DISH = 0x175
    PLASMA_SKULL = 0x176
    PLASMA_FIREBALL = 0x177
    PLASMA_PHOENIX = 0x178
    PLASMA_UNICORN = 0x179
    COUNTRY_NEPAL = 0x17A
    LEVEL_BAMBOO = 0x17B
    LEVEL_BLUEPULSE = 0x17C
    LEVEL_FISH = 0x17D
    LEVEL_GREEN_SPINNIE = 0x17E
    LEVEL_TRACKS = 0x17F
    MISC_ARCADEGO = 0x180
    MISC_CHICKEN = 0x181
    PLASMA_BLUE_SPINNIE = 0x182
    PLASMA_FAWKES = 0x183
    PLASMA_FIST = 0x184
    PLASMA_RED_SPINNIES = 0x185
    PLASMA_SHARK = 0x186
    SPECIAL_CINAMON = 0x187
    SPECIAL_CUPCAKE = 0x188
    SPECIAL_GUMMY = 0x189
    SPECIAL_LOLLIPOP = 0x18A
    SPECIAL_WATERMELON = 0x18B
    LEVEL_TELEPHONE = 0x18C
    LEVEL_MISSILE = 0x18D
    LEVEL_WALL = 0x18E
    PLASMA_UFO = 0x18F
    PLASMA_EYE = 0x190
    PLASMA_RA = 0x191
    SPECIAL_SUMMER_CANOPY = 0x192
    SPECIAL_OASIS = 0x193
    SPECIAL_SUNSET = 0x194
    SPECIAL_WAVE = 0x195
    SPECIAL_SUN = 0x196
    COUNTRY_HAITI = 0x197
    LEVEL_SPIN_CATS = 0x198
    LEVEL_BUBBLES = 0x199
    LEVEL_PUZZLE = 0x19A
    PLASMA_DOT_ILLUSION = 0x19B
    PLASMA_BINARY = 0x19C
    PLASMA_CHIP_SHIP = 0x19D
    SPECIAL_MOON_STARS = 0x19E
    SPECIAL_NIGHT_SKY = 0x19F
    SPECIAL_EIFFEL = 0x1A0
    SPECIAL_AURORA = 0x1A1
    SPECIAL_EARTH_NIGHT = 0x1A2
    LEVEL_BOLTS = 0x1A3
    LEVEL_MANDALA = 0x1A4
    LEVEL_WORMHOLE = 0x1A5
    MISC_HOLE = 0x1A6
    MISC_OREO = 0x1A7
    MISC_RUBIKS = 0x1A8
    PLASMA_INVADERS = 0x1A9
    UNUSED_1 = 0x1AA
    UNUSED_2 = 0x1AB
    UNUSED_3 = 0x1AC
    UNUSED_4 = 0x1AD
    UNUSED_5 = 0x1AE
    UNUSED_6 = 0x1AF
    UNUSED_7 = 0x1B0
    UNUSED_8 = 0x1B1
    UNUSED_9 = 0x1B2
    UNUSED_10 = 0x1B3
    UNUSED_11 = 0x1B4
    UNUSED_12 = 0x1B5
    UNUSED_13 = 0x1B6
    UNUSED_14 = 0x1B7
    UNUSED_15 = 0x1B8
    UNUSED_16 = 0x1B9
    UNUSED_17 = 0x1BA
    UNUSED_18 = 0x1BB
    UNUSED_19 = 0x1BC
    UNUSED_20 = 0x1BD
    UNUSED_21 = 0x1BE
    UNUSED_22 = 0x1BF
    UNUSED_23 = 0x1C0
    UNUSED_24 = 0x1C1
    UNUSED_25 = 0x1C2
    UNUSED_26 = 0x1C3
    PLASMA_PICKAXE = 0x1C4
    PLASMA_PLASMA = 0x1C5
    SPECIAL_DRUM = 0x1C6
    SPECIAL_GUITAR = 0x1C7
    SPECIAL_HORN = 0x1C8
    SPECIAL_OCARINA = 0x1C9
    SPECIAL_PIANO = 0x1CA
    COUNTRY_AFGHANISTAN = 0x1CB
    COUNTRY_SRILANKA = 0x1CC
    ACHIEVE_ARENA_10000 = 0x1CD
    MISC_PURPLE_SMILE = 0x1CE
    MISC_PURPLE_PLANET = 0x1CF
    MISC_SPACE = 0x1D0
    MISC_PULSAR = 0x1D1
    MISC_BLACKHOLE = 0x1D2
    LEVEL_LOCK = 0x1D3
    LEVEL_EYE = 0x1D4
    LEVEL_PENCILS = 0x1D5
    LEVEL_BAT = 0x1D6
    LEVEL_CURSORS = 0x1D7
    ACHIEVE_CW_1000 = 0x1D8
    LEVEL_GALACTIC = 0x1D9
    PLASMA_BEE = 0x1DA
    MISC_DUCK = 0x1DB
    UNUSED_27 = 0x1DC
    TUBER_GAARA = 0x1DD
    UNUSED_28 = 0x1DE
    UNUSED_29 = 0x1DF
    TUBER_BENITEZ = 0x1E0
    TUBER_BADBOY = 0x1E1
    TUBER_PIEDRA = 0x1E2
    UNUSED_30 = 0x1E3
    TUBER_JOHN = 0x1E4
    TUBER_KAMIKAZE = 0x1E5
    UNUSED_31 = 0x1E6
    STANDARD_COTTONCANDY = 0x1E7
    STANDARD_JURASSIC = 0x1E8
    FB_BRASIL = 0x1E9
    COUNTRY_KYRGYZSTAN = 0x1EA
    LEVEL_COLORWHEEL = 0x1EB
    LEVEL_SUNFACE = 0x1EC
    LEVEL_BEE = 0x1ED
    PLASMA_SPINSTER = 0x1EE
    PLASMA_PIZZACUTTER = 0x1EF
    PLASMA_FOSSIL = 0x1F0
    UNUSED_32 = 0x1F1
    TUBER_MAROO = 0x1F2
    TUBER_BLARP = 0x1F3
    TUBER_ROWDY = 0x1F4
    UNUSED_33 = 0x1F5
    TUBER_PRONEBULOUS = 0x1F6
    TUBER_GOKHAN = 0x1F7
    MISC_AMOEBA = 0x1F8
    MISC_NEB_ES = 0x1F9
    MISC_CHRISTMAS = 0x1FA
    MISC_NEB = 0x1FB
    MISC_PANDA_2 = 0x1FC
    MISC_COOKIE_2 = 0x1FD
    LEVEL_SHURIKEN = 0x1FE
    LEVEL_BOW = 0x1FF
    LEVEL_COPTER = 0x200
    LEVEL_MAZE = 0x201
    LEVEL_ARROW = 0x202
    LEVEL_EYE_RAPTOR = 0x203
    LEVEL_EYEBALL = 0x204
    LEVEL_SHURIKEN_2 = 0x205
    LEVEL_HAMMER = 0x206
    LEVEL_BOO1 = 0x207
    MISC_BAUBLE_2 = 0x208
    MISC_NEON = 0x209
    UNUSED_34 = 0x20A
    UNUSED_35 = 0x20B
    UNUSED_36 = 0x20C
    TUBER_KINGS = 0x20D
    LEVEL_UNICORN = 0x20E
    LEVEL_TIGER = 0x20F
    TUBER_TREX = 0x210
    LEVEL_SMOKE = 0x211
    LEVEL_SHELL = 0x212
    LEVEL_EYE_2 = 0x213
    ACHIEVE_SHARK = 0x214
    ACHIEVE_DAB = 0x215
    ACHIEVE_PINWHEEL = 0x216
    MISC_HEARTS = 0x217
    TUBER_CHEETAH = 0x218
    TUBER_NEIKER = 0x219
    TUBER_FENA23 = 0x21A
    TUBER_KOALAOSO = 0x21B
    UNUSED_37 = 0x21C
    FB_ESPANOL = 0x21D
    LEVEL_MOON_2 = 0x21E
    LEVEL_MOON_1 = 0x21F
    LEVEL_GREEN_EMBROIDER = 0x220
    LEVEL_SPIN_RIBBON = 0x221
    LEVEL_NEBGOD = 0x222
    TUBER_JUANGUI = 0x223
    UNUSED_38 = 0x224
    TUBER_SWAG = 0x225
    UNUSED_39 = 0x226
    PLASMA_SWIRLS = 0x227
    PLASMA_YINYANG = 0x228
    PLASMA_TANK = 0x229
    LEVEL_FRACTAL = 0x22A
    LEVEL_HAND = 0x22B
    LEVEL_FIREWHEEL = 0x22C
    LEVEL_FIREPLANE = 0x22D
    LEVEL_PORTAL = 0x22E
    LEVEL_FIREPOWER = 0x22F
    LEVEL_TURTLE = 0x230
    ACHIEVEMENT_BUBBLE = 0x231
    LEVEL_LIQUORICE = 0x232
    LEVEL_PRISM_FLOWER = 0x233
    LEVEL_ILLUSION = 0x234
    MISC_ILLUSION = 0x235
    UNUSED_40 = 0x236
    UNUSED_41 = 0x237
    TUBER_BLACKY = 0x238
    TUBER_RODRICK = 0x239
    LEVEL_SHARK = 0x23A
    PLASMA_ALIEN = 0x23B
    LEVEL_BLUESUN = 0x23C
    ACHIEVE_DOT_GULPER = 0x23D
    PLASMA_WINGS = 0x23E
    MISC_LION_FACE = 0x23F
    MISC_CUTE = 0x240
    LEVEL_PLASMA_COMET = 0x241
    LEVEL_PLASMA = 0x242
    LEVEL_ILLUSION_2 = 0x243
    LEVEL_DRAGONS = 0x244
    LEVEL_COLORWHEEL_2 = 0x245
    LEVEL_ADZE = 0x246
    LEVEL_LEOPARD_2 = 0x247
    LEVEL_FIREFLOWER = 0x248
    PLASMA_HORSE = 0x249
    LEVEL_BIRD = 0x24A
    COUNTRY_BANGLADESH = 0x24B
    PLASMA_FIDGET = 0x24C
    LEVEL_HYDRA = 0x24D
    LEVEL_SKULL = 0x24E
    LEVEL_TRIDENT = 0x24F
    LEVEL_PLASMA_BALL_2 = 0x250
    LEVEL_CRAB = 0x251
    LEVEL_SPIDER = 0x252
    PLASMA_ARTIFACT = 0x253
    LEVEL_ILLUSION_3 = 0x254
    LEVEL_FIDGET = 0x255
    ACHIEVE_FIDGET = 0x256
    PLASMA_FIDGET2 = 0x257
    LEVEL_STAR = 0x258
    LEVEL_CARDIO = 0x259
    LEVEL_GHOST = 0x25A
    LEVEL_GRID = 0x25B
    LEVEL_BULB = 0x25C
    PLASMA_SQUID_1 = 0x25D
    PLASMA_COLORFUL = 0x25E
    LEVEL_CUBES = 0x25F
    LEVEL_CELLS = 0x260
    LEVEL_HOLE_2 = 0x261
    LEVEL_HOLE_3 = 0x262
    LEVEL_PLASMA_SKY = 0x263
    UNUSED_42 = 0x264
    TUBER_TACO = 0x265
    LEVEL_PLASMASTORM = 0x266
    LEVEL_PLASMASTORM_2 = 0x267
    LEVEL_CHAKRAS = 0x268
    LEVEL_PROBE = 0x269
    LEVEL_GLARE = 0x26A
    LEVEL_SWISSCHEESE = 0x26B
    LEVEL_NEBULA = 0x26C
    PLASMA_TARGET = 0x26D
    PLASMA_TRIFIRE = 0x26E
    LEVEL_ARROWS = 0x26F
    MISC_SURREAL = 0x270
    LEVEL_BUBBLES_2 = 0x271
    LEVEL_TURBINE_2 = 0x272
    LEVEL_PULSAR = 0x273
    LEVEL_SHOCKWAVE = 0x274
    LEVEL_PHOENIX = 0x275
    LEVEL_JELLYFISH = 0x276
    PLASMA_BLADES = 0x277
    ACHIEVE_NEBULATOR = 0x278
    ACHIEVE_NEBULATOR_2 = 0x279
    TUBER_MEZO = 0x27A
    LEVEL_PARABOLA = 0x27B
    LEVEL_ORBOROUS = 0x27C
    LEVEL_LEAF = 0x27D
    LEVEL_FAN = 0x27E
    LEVEL_RINGS = 0x27F
    UNUSED_43 = 0x280
    MISC_BULLETHOLE = 0x281
    PLASMA_WHALESHARK = 0x282
    LEVEL_ASTRONAUT = 0x283
    LEVEL_PAW = 0x284
    LEVEL_FALLINGSTARS = 0x285
    LEVEL_BLADES = 0x286
    LEVEL_EMERALDDOVE = 0x287
    LEVEL_PIXELHEART = 0x288
    LEVEL_RAINBOW = 0x289
    LEVEL_FIRETURBINE = 0x28A
    LEVEL_RADIOPLASMA = 0x28B
    LEVEL_FIREBIRD = 0x28C
    LEVEL_FISTBUMP = 0x28D
    LEVEL_EARTHEYE = 0x28E
    LEVEL_VOID = 0x28F
    LEVEL_LIGHTNING = 0x290
    LEVEL_ATOM = 0x291
    LEVEL_FIREDRAGON = 0x292
    LEVEL_COLORPLANE = 0x293
    LEVEL_COLORFIREBALLS = 0x294
    LEVEL_PLASMABLADES = 0x295
    LEVEL_SPINDLE = 0x296
    LEVEL_CONCENTRIC_RINGS = 0x297
    LEVEL_SUNMOONDOG = 0x298
    LEVEL_FIREATOM = 0x299
    LEVEL_FIREWATER = 0x29A
    LEVEL_HOLE_4 = 0x29B
    LEVEL_CYLINDERS = 0x29C
    SPECIAL_PUMPKINDROP = 0x29D
    LEVEL_MAGNI = 0x29E
    SPECIAL_JACK = 0x29F
    LEVEL_ILLUSIONPATTERN = 0x2A0
    SPECIAL_HAND = 0x2A1
    LEVEL_STEALTH = 0x2A2
    LEVEL_LIGHTEXPLOSION = 0x2A3
    LEVEL_ATOM_2 = 0x2A4
    TUBER_NOOB = 0x2A5
    UNUSED_44 = 0x2A6
    SPECIAL_LEAF_WREATH = 0x2A7
    SPECIAL_LEAVES = 0x2A8
    COUNTRY_SINGAPORE = 0x2A9
    LEVEL_SQUARES = 0x2AA
    LEVEL_STARS = 0x2AB
    LEVEL_PLASMA_ARROW = 0x2AC
    XMAS1 = 0x2AD
    XMAS2 = 0x2AE
    XMAS3 = 0x2AF
    XMAS4 = 0x2B0
    XMAS5 = 0x2B1
    XMAS6 = 0x2B2
    XMAS7 = 0x2B3
    XMAS8 = 0x2B4
    XMAS9 = 0x2B5
    XMAS10 = 0x2B6
    XMAS11 = 0x2B7
    XMAS12 = 0x2B8
    XMAS13 = 0x2B9
    XMAS14 = 0x2BA
    XMAS15 = 0x2BB
    XMAS16 = 0x2BC
    XMAS17 = 0x2BD
    XMAS18 = 0x2BE
    XMAS19 = 0x2BF
    XMAS20 = 0x2C0
    XMAS21 = 0x2C1
    XMAS22 = 0x2C2
    XMAS23 = 0x2C3
    XMAS24 = 0x2C4
    XMAS25 = 0x2C5
    XMAS26 = 0x2C6
    XMAS27 = 0x2C7
    SCIFI_URANUS = 0x2C8
    UNUSED_45 = 0x2C9
    TUBER_ORIENTE = 0x2CA
    UNUSED_46 = 0x2CB
    LEVEL_CLOWN_HOLE = 0x2CC
    LEVEL_WOBBLE = 0x2CD
    LEVEL_CARTOON_HOLE = 0x2CE
    LEVEL_NEON_SPINNER = 0x2CF
    LEVEL_LASER_1 = 0x2D0
    ST_ANDRE = 0x2D1
    ST_TACO = 0x2D2
    ST_MEP = 0x2D3
    TUBER_AMANDINHA = 0x2D4
    TUBER_CUCHI = 0x2D5
    ST_MUEKA = 0x2D6
    LEVEL_SPIRAL = 0x2D7
    LEVEL_DRAGONSKIN = 0x2D8
    LEVEL_RGBBULB = 0x2D9
    LEVEL_PSYFLOWER = 0x2DA
    LEVEL_TURBINEFLOWER = 0x2DB
    ST_EXDREAMZ = 0x2DC
    ST_SK = 0x2DD
    LEVEL_RGB = 0x2DE
    LEVEL_ILLUSION_4 = 0x2DF
    LEVEL_PLASMABEAMS = 0x2E0
    LEVEL_RGBPLASMA = 0x2E1
    LEVEL_WHITEHALL = 0x2E2
    ST_EMRE = 0x2E3
    LEVEL_MEANDER = 0x2E4
    LEVEL_PLASMADNA = 0x2E5
    LEVEL_PSITURBINE = 0x2E6
    LEVEL_PANDA = 0x2E7
    LEVEL_GLOWYDONUT = 0x2E8
    LEVEL_EMOJIS = 0x2E9
    SPECIAL_EGG = 0x2EA
    LEVEL_ILLUSION_5 = 0x2EB
    LEVEL_FLOWERSPIRAL = 0x2EC
    LEVEL_SQUARESPIRAL = 0x2ED
    LEVEL_PLASMATILE = 0x2EE
    LEVEL_ARROWINDER = 0x2EF
    LEVEL_FIRETWIRL = 0x2F0
    LEVEL_RGBALL = 0x2F1
    LEVEL_RGBTURBINE = 0x2F2
    UNUSED_47 = 0x2F3
    LEVEL_FLY = 0x2F4
    LEVEL_PURPLEHOLE = 0x2F5
    LEVEL_FIREPLANT = 0x2F6
    LEVEL_BALLOON = 0x2F7
    LEVEL_GREENSTAR = 0x2F8
    COUNTRY_CAMBODIA = 0x2F9
    LEVEL_FACE = 0x2FA
    LEVEL_BUBBLEMOUSE = 0x2FB
    LEVEL_OSCOPE = 0x2FC
    LEVEL_HANGLOOSE = 0x2FD
    MISC_RIBBON = 0x2FE
    LEVEL_PURPLE_SPINNY = 0x2FF
    LEVEL_BEACHBALL = 0x300
    LEVEL_MARBLE = 0x301
    LEVEL_SUNBALL = 0x302
    LEVEL_BALL = 0x303
    LEVEL_BLANK = 0x304
    LEVEL_JADEFLOWER = 0x305
    LEVEL_RETROSWIRL = 0x306
    PLASMA_DOGGY = 0x307
    LEVEL_MANDALA_2 = 0x308
    LEVEL_SQUARE_SPIRAL = 0x309
    LEVEL_WORMHOLE_2 = 0x30A
    LEVEL_PLANTBUBBLE = 0x30B
    LEVEL_ROCKETSHIP = 0x30C
    LEVEL_MOBIUS = 0x30D
    LEVEL_REDBLUE_SPIRAL = 0x30E
    TUBER_REVOLTZ = 0x30F
    LEVEL_GIF1_FRAME0 = 0x310
    LEVEL_GIF2_FRAME0 = 0x311
    LEVEL_GIF3_FRAME0 = 0x312
    MISC_GRAPEFRUIT = 0x313
    LEVEL_EARTHSTAR = 0x314
    LEVEL_GLASSFLOWER = 0x315
    LEVEL_FACES = 0x316
    LEVEL_GOLDLATTICE = 0x317
    LEVEL_GIF4_FRAME0 = 0x318
    LEVEL_PSYSUN = 0x319
    MISC_GALAXY = 0x31A
    LEVEL_MOLTENARMOR = 0x31B
    LEVEL_PAINTSPLOSION = 0x31C
    ST_VICTOR = 0x31D
    TUBER_MOISES = 0x31E
    LEVEL_PURPLEBUBBLES = 0x31F
    LEVEL_RGBVORTEX = 0x320
    LEVEL_EYEFLOWER = 0x321
    TUBER_PESADELO = 0x322
    LEVEL_ENERGY = 0x323
    MISC_SPACEROSE = 0x324
    PLASMA_DEADMAU5 = 0x325
    LEVEL_GIF5_FRAME0 = 0x326
    ST_INDEX = 0x327
    LEVEL_MAGNETICFIELD = 0x328
    LEVEL_GIF6_FRAME0 = 0x329
    LEVEL_FRACTAL_2 = 0x32A
    LEVEL_BOOMERANG = 0x32B
    LEVEL_KITTYCAT = 0x32C
    MISC_GREENSTAR = 0x32D
    LEVEL_PURPLESHELL = 0x32E
    LEVEL_PULSE = 0x32F
    LEVEL_PURPLEPULSAR = 0x330
    PACK_GHOST = 0x331
    PACK_EYE = 0x332
    PACK_SKELETON = 0x333
    PACK_JACK = 0x334
    PACK_HALLOWEEN = 0x335
    LEVEL_TRIPPY = 0x336
    LEVEL_LOOK = 0x337
    LEVEL_GIF7_FRAME0 = 0x338
    LEVEL_GIF8_FRAME0 = 0x339
    MISC_STAR_SPIRAL = 0x33A
    LEVEL_HAPPYSTARS = 0x33B
    LEVEL_BLUEDISC = 0x33C
    LEVEL_PLASMAYANG = 0x33D
    LEVEL_ABSTRACTTURBINE = 0x33E
    LEVEL_GIF9_FRAME0 = 0x33F
    STANDARD_GALAXYGLOBE = 0x340
    LEVEL_PURPLELIGHTNING = 0x341
    LEVEL_NEBRINGS = 0x342
    LEVEL_GIF10_FRAME0 = 0x343
    LEVEL_METALMAZE = 0x344
    PACK_XMAS = 0x345
    PACK_SNOW = 0x346
    PACK_SANTA = 0x347
    PACK_SNOWFLAKE = 0x348
    PACK_CANDYTOWN = 0x349
    STANDARD_ILLUSION = 0x34A
    LEVEL_TURBINE_STARS = 0x34B
    LEVEL_RED_VORTEX = 0x34C
    LEVEL_WATERBOWL = 0x34D
    STANDARD_XMAS15 = 0x34E
    STANDARD_NEWYEAR16 = 0x34F
    STANDARD_XMAS16 = 0x350
    STANDARD_NEWYEAR17 = 0x351
    STANDARD_XMAS17 = 0x352
    STANDARD_NEWYEAR18 = 0x353
    STANDARD_XMAS18 = 0x354
    STANDARD_NEWYEAR19 = 0x355
    LEVEL_GIF11_FRAME0 = 0x356
    STANDARD_REDFALLS = 0x357
    LEVEL_ENERGYSHIELD = 0x358
    LEVEL_PRISMZOOM = 0x359
    LEVEL_LIGHTNINGBALL = 0x35A
    PACK_VDAY = 0x35B
    PACK_HEART = 0x35C
    PACK_CUPID = 0x35D
    PACK_BOUQUET = 0x35E
    PACK_BLOOM_FRAME0 = 0x35F
    PACK_BOW_1 = 0x360
    STANDARD_PEACOCKTAIL = 0x361
    LEVEL_GOLDENRING = 0x362
    LEVEL_PURPLEPHOENIX = 0x363
    LEVEL_GOLDENRING2 = 0x364
    LEVEL_GIF12_FRAME0 = 0x365
    LEVEL_BLUETURBINE = 0x366
    LEVEL_STARDUST = 0x367
    LEVEL_SKULLFLOWER = 0x368
    STANDARD_STRAWBERRY = 0x369
    TUBER_AGNOZIA = 0x36A
    ACHIEVE_VET_1 = 0x36B
    ACHIEVE_VET_2 = 0x36C
    ACHIEVE_VET_3 = 0x36D
    ACHIEVE_VET_4 = 0x36E
    ACHIEVE_VET_5 = 0x36F
    LEVEL_UFOS = 0x370
    LEVEL_NEBUNAUT = 0x371
    LEVEL_ROSEY = 0x372
    LEVEL_FIREFLOWER2 = 0x373
    LEVEL_BLUESTAR = 0x374
    LEVEL_FIREHORSE = 0x375
    LEVEL_GIF13_FRAME0 = 0x376
    PLASMA_PLASMA_BALL = 0x377
    UNUSED_48 = 0x378
    LEVEL_PURPLESPIRAL = 0x379
    LEVEL_PSIFLOWER = 0x37A
    LEVEL_FIREBIRDY = 0x37B
    STANDARD_1 = 0x37C
    STANDARD_2 = 0x37D
    STANDARD_3 = 0x37E
    STANDARD_4 = 0x37F
    STANDARD_5 = 0x380
    STANDARD_6 = 0x381
    STANDARD_7 = 0x382
    STANDARD_8 = 0x383
    STANDARD_9 = 0x384
    STANDARD_10 = 0x385
    STANDARD_11 = 0x386
    STANDARD_12 = 0x387
    STANDARD_13 = 0x388
    STANDARD_14 = 0x389
    STANDARD_15 = 0x38A
    STANDARD_16 = 0x38B
    STANDARD_17 = 0x38C
    STANDARD_18 = 0x38D
    STANDARD_19 = 0x38E
    STANDARD_20 = 0x38F
    STANDARD_21 = 0x390
    STANDARD_22 = 0x391
    STANDARD_23 = 0x392
    STANDARD_24 = 0x393
    STANDARD_25 = 0x394
    STANDARD_26 = 0x395
    STANDARD_27 = 0x396
    STANDARD_28 = 0x397
    STANDARD_29 = 0x398
    STANDARD_30 = 0x399
    LEVEL_FIRE_WHEEL = 0x39A
    LEVEL_ICE_WHEEL = 0x39B
    LEVEL_WATER_WHEEL = 0x39C
    LEVEL_MOSKULL = 0x39D
    LEVEL_RGBPLANE = 0x39E
    LEVEL_RGB_TURBINE = 0x39F
    LEVEL_GOLDEN_GLOW = 0x3A0
    LEVEL_PUZZLE_PIECES = 0x3A1
    LEVEL_POPO = 0x3A2
    LEVEL_GIF14_FRAME0 = 0x3A3
    STANDARD_31 = 0x3A4
    STANDARD_32 = 0x3A5
    STANDARD_33 = 0x3A6
    STANDARD_34 = 0x3A7
    STANDARD_35 = 0x3A8
    STANDARD_36 = 0x3A9
    STANDARD_37 = 0x3AA
    STANDARD_38 = 0x3AB
    STANDARD_39 = 0x3AC
    STANDARD_40 = 0x3AD
    STANDARD_41 = 0x3AE
    STANDARD_42 = 0x3AF
    STANDARD_43 = 0x3B0
    STANDARD_44 = 0x3B1
    STANDARD_45 = 0x3B2
    STANDARD_46 = 0x3B3
    STANDARD_47 = 0x3B4
    STANDARD_48 = 0x3B5
    STANDARD_49 = 0x3B6
    STANDARD_50 = 0x3B7
    ST_FERDIOS = 0x3B8
    LEVEL_PEACOCK = 0x3B9
    LEVEL_HADRON = 0x3BA
    LEVEL_WAVY = 0x3BB
    LEVEL_BLOODTURBINE = 0x3BC
    LEVEL_GIF15_FRAME0 = 0x3BD
    STANDARD_51 = 0x3BE
    LEVEL_WAVY_RGB = 0x3BF
    LEVEL_FLICKERSKULL = 0x3C0
    LEVEL_SNOWTURBINE = 0x3C1
    LEVEL_LAVATURBINE = 0x3C2
    LEVEL_GRASSTURBINE = 0x3C3
    LEVEL_TRIPPYPURP = 0x3C4
    LEVEL_TRIPPYTEAL = 0x3C5
    LEVEL_PLASMASWIRL = 0x3C6
    ACHIEVE_GIF16_FRAME0 = 0x3C7
    LEVEL_PURPLEFEATHERS = 0x3C8
    LEVEL_BLUEFLOWERS = 0x3C9
    LEVEL_ANCHORAGE = 0x3CA
    STANDARD_SPACEFACE = 0x3CB
    LEVEL_NEUROTICNEBULA = 0x3CC
    LEVEL_DIGITALWATERFALL = 0x3CD
    LEVEL_WOBBLESPIN = 0x3CE
    LEVEL_STAINEDFRACTAL = 0x3CF
    COUNTRY_VIETNAM = 0x3D0
    LEVEL_GOLDHALO = 0x3D1
    LEVEL_PRISMATICDISC = 0x3D2
    LEVEL_MADAVIAN = 0x3D3
    TUBER_STEN = 0x3D4
    TUBER_SNAY = 0x3D5
    TUBER_KLEZXVERS = 0x3D6
    LEVEL_SKULLBONES = 0x3D7
    LEVEL_COLORSTAR = 0x3D8
    LEVEL_SYMMETRY = 0x3D9
    LEVEL_ENTROPY = 0x3DA
    TUBER_BADGIRL = 0x3DB
    TUBER_FUTURDROIDBR = 0x3DC
    TUBER_MELENNIE = 0x3DD
    TUBER_KEEIZ = 0x3DE
    TUBER_KOJI = 0x3DF
    LEVEL_GIF16_FRAME0 = 0x3E0
    COUNTRY_OMAN = 0x3E1
    TUBER_DANZIN = 0x3E2
    LEVEL_DAB = 0x3E3
    STANDARD_PLASMABALL = 0x3E4
    LEVEL_FIREGALAXY = 0x3E5
    LEVEL_ELECTROBAUBLE = 0x3E6
    LEVEL_LEOPARDSKIN = 0x3E7
    LEVEL_ORBOROUS2 = 0x3E8
    LEVEL_GREEN_PLASMA = 0x3E9
    LEVEL_ELECTRIC_PLASMA = 0x3EA
    TUBER_ABSALOM = 0x3EB
    STANDARD_52 = 0x3EC
    STANDARD_53 = 0x3ED
    LEVEL_BINARY_SPIRAL = 0x3EE
    LEVEL_SUN = 0x3EF
    LEVEL_LIGHTBALL = 0x3F0
    LEVEL_BLUESPARK = 0x3F1
    LEVEL_BEETLE = 0x3F2
    LEVEL_EYES = 0x3F3
    STANDARD_SPACEMARBLE = 0x3F4
    LEVEL_DANDYLION = 0x3F5
    LEVEL_SHUTTLECRAFT = 0x3F6
    LEVEL_REDSPARK = 0x3F7
    LEVEL_PASTEL = 0x3F8
    ACHIEVE_VET_6 = 0x3F9
    LEVEL_WAVYTWIST = 0x3FA
    LEVEL_MOUSE_POINTER = 0x3FB
    LEVEL_MOUSE_HOURGLASS = 0x3FC
    PLASMA_NOOB = 0x3FD
    LEVEL_CHICKEN = 0x3FE
    LEVEL_PIZZA = 0x3FF
    LEVEL_PEARL = 0x400
    COUNTRY_SURINAME = 0x401
    LEVEL_COLORBALLS = 0x402
    STANDARD_PURPLEGALAXY = 0x403
    LEVEL_APPLE = 0x404
    LEVEL_FIREFOOTBALL = 0x405
    STANDARD_54 = 0x406
    LEVEL_PINKSWIRL = 0x407
    LEVEL_NAUTILUS = 0x408
    LEVEL_SPACESYMBOLS = 0x409
    COUNTRY_LIBYA = 0x40A
    COUNTRY_MAURITANIA = 0x40B
    COUNTRY_SOMALIA = 0x40C
    COUNTRY_PALESTINE = 0x40D
    COUNTRY_COMOROS = 0x40E
    COUNTRY_DJIBOUTI = 0x40F
    COUNTRY_SUDAN = 0x410
    LEVEL_TRIBALBIRD = 0x411
    LEVEL_DARKPURPLESPINNER = 0x412
    LEVEL_DARKORANGETESSELATE = 0x413
    COUNTRY_EQUATORIAL_GUINEA = 0x414
    STANDARD_ROBL = 0x415
    TUBER_MOODI = 0x416
    TUBER_VIPER = 0x417
    ACHIEVE_VET_7 = 0x418
    TUBER_MBB = 0x419
    ST_MAJA = 0x41A
    ST_CEDRIC = 0x41B
    ST_SARONIX = 0x41C
    LEVEL_JWST_1 = 0x41D
    LEVEL_JWST_2 = 0x41E
    STANDARD_55 = 0x41F
    ST_DCDUDE = 0x420
    ST_JORGE = 0x421
    TUBER_ELYES = 0x422
    TUBER_TURKI = 0x423
    PACK_RAMADAN_SKIN_1 = 0x424
    PACK_RAMADAN_SKIN_2 = 0x425
    PACK_RAMADAN_SKIN_3 = 0x426
    PACK_RAMADAN_SKIN_4 = 0x427
    PACK_RAMADAN_SKIN_5 = 0x428
    ST_ANGEL = 0x429
    ACHIEVE_VET_8 = 0x42A
    LEVEL_FINAL = 0x42B
    PLASMA_LEGEND = 0x42C
    ACHIEVE_VET_9 = 0x42D


class ParitcleType(enum.Enum):
    PARTICLE_1 = 0x00
    PARTICLE_2 = 0x01
    PARTICLE_3 = 0x02
    PARTICLE_4 = 0x03
    PARTICLE_5 = 0x04
    PARTICLE_6 = 0x05
    PARTICLE_7 = 0x06
    PARTICLE_8 = 0x07
    PARTICLE_9 = 0x08
    PARTICLE_10 = 0x09
    PARTICLE_11 = 0x0A
    PARTICLE_12 = 0x0B
    PARTICLE_13 = 0x0C
    PARTICLE_14 = 0x0D
    PARTICLE_15 = 0x0E
    PARTICLE_16 = 0x0F
    PARTICLE_17 = 0x10
    PARTICLE_18 = 0x11
    PARTICLE_19 = 0x12
    PARTICLE_20 = 0x13
    PARTICLE_21 = 0x14
    PARTICLE_22 = 0x15
    PARTICLE_23 = 0x16
    PARTICLE_24 = 0x17
    PARTICLE_25 = 0x18
    PARTICLE_26 = 0x19
    PARTICLE_27 = 0x1A
    PARTICLE_28 = 0x1B
    PARTICLE_29 = 0x1C
    PARTICLE_30 = 0x1D
    PARTICLE_31 = 0x1E
    PARTICLE_32 = 0x1F
    PARTICLE_33 = 0x20
    PARTICLE_34 = 0x21
    PARTICLE_35 = 0x22
    PARTICLE_36 = 0x23
    PARTICLE_37 = 0x24
    PARTICLE_NONE = -0x01


class PetType(enum.Enum):
    PET_0 = 0x00
    PET_1 = 0x01
    PET_2 = 0x02
    PET_3 = 0x03
    PET_4 = 0x04
    PET_5 = 0x05
    PET_6 = 0x06
    PET_7 = 0x07
    PET_8 = 0x08
    PET_9 = 0x09
    PET_10 = 0x0A
    PET_11 = 0x0B
    PET_12 = 0x0C
    PET_13 = 0x0D
    PET_14 = 0x0E
    PET_15 = 0x0F
    PET_16 = 0x10
    PET_17 = 0x11
    PET_18 = 0x12
    PET_19 = 0x13
    PET_20 = 0x14
    PET_21 = 0x15
    PET_22 = 0x16
    PET_23 = 0x17
    PET_24 = 0x18
    PET_25 = 0x19
    PET_26 = 0x1A
    PET_27 = 0x1B
    PET_28 = 0x1C
    PET_29 = 0x1D
    PET_30 = 0x1E
    PET_31 = 0x1F
    PET_32 = 0x20
    PET_33 = 0x21
    PET_34 = 0x22
    PET_35 = 0x23
    PET_36 = 0x24
    PET_37 = 0x25
    PET_38 = 0x26
    PET_39 = 0x27
    PET_40 = 0x28
    PET_41 = 0x29
    PET_42 = 0x2A
    PET_43 = 0x2B
    PET_44 = 0x2C
    PET_45 = 0x2D
    PET_46 = 0x2E
    PET_47 = 0x2F
    PET_48 = 0x30
    PET_49 = 0x31
    PET_50 = 0x32
    PET_51 = 0x33
    PET_52 = 0x34
    PET_53 = 0x35
    PET_54 = 0x36
    PET_55 = 0x37
    PET_56 = 0x38
    PET_57 = 0x39
    PET_58 = 0x3A
    PET_59 = 0x3B
    PET_60 = 0x3C
    PET_61 = 0x3D
    PET_62 = 0x3E
    PET_63 = 0x3F
    PET_64 = 0x40
    PET_65 = 0x41
    PET_66 = 0x42
    PET_67 = 0x43
    PET_68 = 0x44
    PET_69 = 0x45
    PET_70 = 0x46
    PET_71 = 0x47
    PET_72 = 0x48
    PET_73 = 0x49
    PET_74 = 0x4A
    PET_75 = 0x4B
    PET_76 = 0x4C
    PET_77 = 0x4D
    PET_78 = 0x4E
    PET_79 = 0x4F
    PET_80 = 0x50
    PET_81 = 0x51
    PET_82 = 0x52
    PET_83 = 0x53
    PET_84 = 0x54
    PET_85 = 0x55
    PET_NONE = -0x01


class PetRopeType(enum.Enum):
    ROPE0 = 0x00
    ROPE1 = 0x01
    ROPE2 = 0x02
    ROPE3 = 0x03
    ROPE4 = 0x04
    ROPE5 = 0x05
    ROPE6 = 0x06
    ROPE7 = 0x07
    ROPE8 = 0x08
    ROPE9 = 0x09
    ROPE10 = 0x0A
    ROPE11 = 0x0B
    ROPE12 = 0x0C
    ROPE13 = 0x0D
    ROPE14 = 0x0E
    ROPE15 = 0x0F
    ROPE16 = 0x10
    ROPE17 = 0x11
    ROPE18 = 0x12
    ROPE19 = 0x13
    ROPE20 = 0x14
    ROPE21 = 0x15
    ROPE22 = 0x16
    ROPE23 = 0x17
    ROPE24 = 0x18
    ROPE25 = 0x19
    ROPE26 = 0x1A
    ROPE27 = 0x1B
    ROPE28 = 0x1C
    ROPE29 = 0x1D
    ROPE30 = 0x1E
    ROPE31 = 0x1F
    ROPE32 = 0x20
    ROPE33 = 0x21
    ROPE34 = 0x22
    ROPE35 = 0x23
    ROPE36 = 0x24
    ROPE37 = 0x25
    ROPE38 = 0x26
    ROPE39 = 0x27
    ROPE40 = 0x28
    ROPE41 = 0x29
    ROPE42 = 0x2A
    ROPE43 = 0x2B
    ROPE44 = 0x2C
    ROPE45 = 0x2D
    ROPE46 = 0x2E
    ROPE47 = 0x2F
    ROPE48 = 0x30
    ROPE49 = 0x31
    ROPE50 = 0x32
    ROPE51 = 0x33
    ROPE52 = 0x34
    ROPE53 = 0x35
    ROPE54 = 0x36
    ROPE55 = 0x37
    ROPE56 = 0x38
    ROPE57 = 0x39
    ROPE58 = 0x3A
    ROPE59 = 0x3B
    ROPE60 = 0x3C
    ROPE61 = 0x3D
    ROPE62 = 0x3E
    ROPE63 = 0x3F
    ROPE64 = 0x40
    ROPE65 = 0x41
    ROPE66 = 0x42
    ROPE67 = 0x43
    ROPE68 = 0x44
    ROPE69 = 0x45
    ROPE70 = 0x46
    ROPE_NONE = -0x01


class HatType(enum.Enum):
    HAT_1 = 0x00
    HAT_2 = 0x01
    HAT_3 = 0x02
    HAT_4 = 0x03
    HAT_5 = 0x04
    HAT_6 = 0x05
    HAT_7 = 0x06
    HAT_8 = 0x07
    HAT_9 = 0x08
    HAT_10 = 0x09
    HAT_11 = 0x0A
    HAT_12 = 0x0B
    HAT_13 = 0x0C
    HAT_14 = 0x0D
    HAT_15 = 0x0E
    HAT_16 = 0x0F
    HAT_17 = 0x10
    HAT_18 = 0x11
    HAT_19 = 0x12
    HAT_20 = 0x13
    HAT_21 = 0x14
    HAT_22 = 0x15
    HAT_23 = 0x16
    HAT_24 = 0x17
    HAT_25 = 0x18
    HAT_26 = 0x19
    HAT_27 = 0x1A
    HAT_28 = 0x1B
    HAT_29 = 0x1C
    HAT_30 = 0x1D
    HAT_31 = 0x1E
    HAT_32 = 0x1F
    HAT_33 = 0x20
    HAT_34 = 0x21
    HAT_35 = 0x22
    HAT_36 = 0x23
    HAT_37 = 0x24
    HAT_38 = 0x25
    HAT_39 = 0x26
    HAT_40 = 0x27
    HAT_41 = 0x28
    HAT_42 = 0x29
    HAT_43 = 0x2A
    HAT_44 = 0x2B
    HAT_45 = 0x2C
    HAT_46 = 0x2D
    HAT_47 = 0x2E
    HAT_48 = 0x2F
    HAT_49 = 0x30
    HAT_50 = 0x31
    HAT_51 = 0x32
    HAT_52 = 0x33
    HAT_53 = 0x34
    HAT_54 = 0x35
    HAT_55 = 0x36
    HAT_56 = 0x37
    HAT_57 = 0x38
    HAT_58 = 0x39
    HAT_59 = 0x3A
    HAT_60 = 0x3B
    HAT_61 = 0x3C
    HAT_62 = 0x3D
    HAT_63 = 0x3E
    HAT_64 = 0x3F
    HAT_65 = 0x40
    HAT_66 = 0x41
    HAT_67 = 0x42
    HAT_68 = 0x43
    HAT_69 = 0x44
    HAT_70 = 0x45
    HAT_71 = 0x46
    HAT_72 = 0x47
    HAT_73 = 0x48
    HAT_74 = 0x49
    HAT_75 = 0x4A
    HAT_76 = 0x4B
    HAT_77 = 0x4C
    HAT_78 = 0x4D
    HAT_79 = 0x4E
    HAT_80 = 0x4F
    HAT_81 = 0x50
    HAT_82 = 0x51
    HAT_83 = 0x52
    HAT_84 = 0x53
    HAT_85 = 0x54
    HAT_86 = 0x55
    HAT_87 = 0x56
    HAT_88 = 0x57
    HAT_89 = 0x58
    HAT_90 = 0x59
    HAT_91 = 0x5A
    HAT_92 = 0x5B
    HAT_93 = 0x5C
    HAT_94 = 0x5D
    HAT_95 = 0x5E
    HAT_96 = 0x5F
    HAT_97 = 0x60
    HAT_98 = 0x61
    HAT_99 = 0x62
    HAT_100 = 0x63
    HAT_101 = 0x64
    HAT_102 = 0x65
    HAT_103 = 0x66
    HAT_104 = 0x67
    HAT_105 = 0x68
    HAT_NONE = -0x01


class HaloType(enum.Enum):
    HALO_1 = 0x00
    HALO_2 = 0x01
    HALO_3 = 0x02
    HALO_4 = 0x03
    HALO_5 = 0x04
    HALO_6 = 0x05
    HALO_7 = 0x06
    HALO_8 = 0x07
    HALO_9 = 0x08
    HALO_10 = 0x09
    HALO_11 = 0x0A
    HALO_12 = 0x0B
    HALO_13 = 0x0C
    HALO_14 = 0x0D
    HALO_15 = 0x0E
    HALO_16 = 0x0F
    HALO_17 = 0x10
    HALO_18 = 0x11
    HALO_19 = 0x12
    HALO_20 = 0x13
    HALO_21 = 0x14
    HALO_22 = 0x15
    HALO_23 = 0x16
    HALO_24 = 0x17
    HALO_25 = 0x18
    HALO_26 = 0x19
    HALO_27 = 0x1A
    HALO_28 = 0x1B
    HALO_29 = 0x1C
    HALO_30 = 0x1D
    HALO_31 = 0x1E
    HALO_32 = 0x1F
    HALO_33 = 0x20
    HALO_34 = 0x21
    HALO_35 = 0x22
    HALO_36 = 0x23
    HALO_37 = 0x24
    HALO_38 = 0x25
    HALO_39 = 0x26
    HALO_40 = 0x27
    HALO_41 = 0x28
    HALO_42 = 0x29
    HALO_43 = 0x2A
    HALO_44 = 0x2B
    HALO_45 = 0x2C
    HALO_46 = 0x2D
    HALO_47 = 0x2E
    HALO_48 = 0x2F
    HALO_49 = 0x30
    HALO_50 = 0x31
    HALO_51 = 0x32
    HALO_52 = 0x33
    HALO_53 = 0x34
    HALO_NONE = -0x01


class EjectSkinType(enum.Enum):
    EJECT_0 = 0x00
    EJECT_1 = 0x01
    EJECT_2 = 0x02
    EJECT_3 = 0x03
    EJECT_4 = 0x04
    EJECT_5 = 0x05
    EJECT_6 = 0x06
    EJECT_7 = 0x07
    EJECT_8 = 0x08
    EJECT_9 = 0x09
    EJECT_10 = 0x0A
    EJECT_11 = 0x0B
    EJECT_12 = 0x0C
    EJECT_13 = 0x0D
    EJECT_14 = 0x0E
    EJECT_15 = 0x0F
    EJECT_16 = 0x10
    EJECT_17 = 0x11
    EJECT_18 = 0x12
    EJECT_19 = 0x13
    EJECT_20 = 0x14
    EJECT_21 = 0x15
    EJECT_22 = 0x16
    EJECT_23 = 0x17
    EJECT_24 = 0x18
    EJECT_25 = 0x19
    EJECT_26 = 0x1A
    EJECT_27 = 0x1B
    EJECT_28 = 0x1C
    EJECT_29 = 0x1D
    EJECT_30 = 0x1E
    EJECT_31 = 0x1F
    EJECT_32 = 0x20
    EJECT_33 = 0x21
    EJECT_34 = 0x22
    EJECT_35 = 0x23
    EJECT_36 = 0x24
    EJECT_37 = 0x25
    EJECT_38 = 0x26
    EJECT_39 = 0x27
    EJECT_40 = 0x28
    EJECT_41 = 0x29
    EJECT_42 = 0x2A
    EJECT_43 = 0x2B
    EJECT_NONE = -0x01


class EmoteType(enum.Enum):
    EMOTE_1 = 0x00
    EMOTE_2 = 0x01
    EMOTE_3 = 0x02
    EMOTE_4 = 0x03
    EMOTE_5 = 0x04
    EMOTE_6 = 0x05
    EMOTE_7 = 0x06
    EMOTE_8 = 0x07
    EMOTE_9 = 0x08
    EMOTE_10 = 0x09
    EMOTE_11 = 0x0A
    EMOTE_12 = 0x0B
    EMOTE_13 = 0x0C
    EMOTE_14 = 0x0D
    EMOTE_15 = 0x0E
    EMOTE_16 = 0x0F
    EMOTE_17 = 0x10
    EMOTE_18 = 0x11
    EMOTE_19 = 0x12
    EMOTE_20 = 0x13
    EMOTE_21 = 0x14
    EMOTE_22 = 0x15
    EMOTE_23 = 0x16
    EMOTE_24 = 0x17
    EMOTE_25 = 0x18
    EMOTE_26 = 0x19
    EMOTE_27 = 0x1A
    EMOTE_28 = 0x1B
    EMOTE_29 = 0x1C
    EMOTE_30 = 0x1D
    EMOTE_31 = 0x1E
    EMOTE_32 = 0x1F
    EMOTE_33 = 0x20
    EMOTE_34 = 0x21
    EMOTE_35 = 0x22
    EMOTE_36 = 0x23
    EMOTE_37 = 0x24
    EMOTE_38 = 0x25
    EMOTE_39 = 0x26
    EMOTE_40 = 0x27
    EMOTE_41 = 0x28
    EMOTE_42 = 0x29
    EMOTE_43 = 0x2A
    EMOTE_44 = 0x2B
    EMOTE_45 = 0x2C
    EMOTE_46 = 0x2D
    EMOTE_47 = 0x2E
    EMOTE_48 = 0x2F
    EMOTE_49 = 0x30
    EMOTE_50 = 0x31
    EMOTE_51 = 0x32
    EMOTE_52 = 0x33
    EMOTE_53 = 0x34
    EMOTE_54 = 0x35
    EMOTE_55 = 0x36
    EMOTE_56 = 0x37
    EMOTE_57 = 0x38
    EMOTE_58 = 0x39
    EMOTE_59 = 0x3A
    EMOTE_60 = 0x3B
    EMOTE_61 = 0x3C
    EMOTE_62 = 0x3D
    EMOTE_63 = 0x3E
    EMOTE_64 = 0x3F
    EMOTE_65 = 0x40
    EMOTE_66 = 0x41
    EMOTE_67 = 0x42
    EMOTE_68 = 0x43
    EMOTE_69 = 0x44
    EMOTE_70 = 0x45
    EMOTE_71 = 0x46
    EMOTE_72 = 0x47
    EMOTE_73 = 0x48
    EMOTE_74 = 0x49
    EMOTE_75 = 0x4A
    EMOTE_76 = 0x4B
    EMOTE_77 = 0x4C
    EMOTE_78 = 0x4D
    EMOTE_79 = 0x4E
    EMOTE_80 = 0x4F
    EMOTE_81 = 0x50
    EMOTE_82 = 0x51
    EMOTE_83 = 0x52
    EMOTE_84 = 0x53
    EMOTE_85 = 0x54
    EMOTE_86 = 0x55
    EMOTE_87 = 0x56
    EMOTE_88 = 0x57
    EMOTE_89 = 0x58
    EMOTE_90 = 0x59
    EMOTE_91 = 0x5A
    EMOTE_92 = 0x5B


class PresentType(enum.Enum):
    PRESENT1 = 0x00
    PRESENT2 = 0x01
    PRESENT3 = 0x02
    PRESENT4 = 0x03
    PRESENT5 = 0x04
    PRESENT6 = 0x05
