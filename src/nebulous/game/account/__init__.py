from __future__ import annotations

import base64
import logging
from dataclasses import dataclass, field
from enum import StrEnum
from http import HTTPStatus
from typing import Any, ClassVar

import requests

from nebulous.game import constants
from nebulous.game.enums import (
    ClanRole,
    CustomSkinStatus,
    CustomSkinType,
    Font,
    GameMode,
    Item,
    ProfileVisibility,
    PurchasableType,
    Relationship,
    SaleType,
    Skin,
    SpinType,
)
from nebulous.game.exceptions import InvalidMailIDError, InvalidUserIDError, NotSignedInError
from nebulous.game.models.apiobjects import (
    APICheckinResult,
    APICoinPurchaseResult,
    APIPlayerGeneralStats,
    APIPlayerProfile,
    APIPlayerStats,
    APISaleInfo,
    APISkin,
    APISkinData,
    APISkinIDs,
    APISkinURLBase,
    Clan,
    ClanMember,
    PlayerTitles,
)


class ServerRegions(StrEnum):
    US_WEST = "US_WEST"
    US_EAST = "US_EAST"
    EU = "EU"
    EAST_ASIA = "EAST_ASIA"
    SOUTH_AMERICA = "SOUTH_AMERICA"
    AUSTRALIA = "AUSTRALIA"
    SOUTH_ASIA = "SOUTH_ASIA"
    MIDDLE_EAST = "MIDDLE_EAST"
    INDIA = "INDIA"
    SOUTH_AFRICA = "SOUTH_AFRICA"
    JAPAN = "JAPAN"
    DEBUG = "DEBUG"
    DEBUG_GLOBAL = "DEBUG_GLOBAL"


class Endpoints(StrEnum):
    """Endpoints for the Nebulous API."""

    SECURE_TICKET = "JDKaYIIScQ"
    GET_PLAYER_PROFILE = "GetPlayerProfile"
    GET_MAIL_LIST = "GetMailList"
    READ_MAIL = "ReadMail"
    SEND_MAIL = "SendMail"
    DELETE_MAIL = "DeleteMail"
    ADD_FRIEND = "AddFriend"
    GET_FRIENDS = "GetFriends"
    GET_PLAYER_STATS = "GetPlayerStats"
    GET_SKIN_IDS = "GetSkinIDs"
    GET_SALE_INFO = "GetSaleInfo"
    GET_SKIN_URL_BASE = "GetSkinURLBase"
    GET_PURCHASE_PRICES = "GetPurchasePrices"
    COIN_PURCHASE = "CoinPurchase"
    GET_SKIN_DATA = "GetSkinData"
    CHECKIN = "CheckIn"
    GET_SPIN_INFO = "GetSpinInfo"


@dataclass
class AccountObject:
    account: Account  # represents the current signed in account


@dataclass
class APIPlayer(AccountObject):
    account_id: int

    def get_profile(self) -> APIPlayerProfile:
        if self.account_id < 0:
            raise InvalidUserIDError("Cannot fetch profile without a valid account ID.")

        return self.account.get_player_profile(self.account_id)

    def get_stats(self) -> APIPlayerStats:
        if self.account_id < 0:
            raise InvalidUserIDError("Cannot fetch stats without a valid account ID.")

        return self.account.get_player_stats(self.account_id)

    @classmethod
    def from_account_id(cls, account: Account, account_id: int) -> APIPlayer:
        if account_id < 0:
            raise InvalidUserIDError("Invalid account ID.")

        return cls(account, account_id)


@dataclass
class APIFriend(APIPlayer):
    relationship: Relationship
    bff: bool
    last_played_utc: str


@dataclass
class APIMailEnvelope(AccountObject):
    msg_id: int
    from_aid: int
    to_aid: int
    to_name: str
    from_name: str
    subject: str
    is_new: bool
    time_sent: str
    time_expires: str
    to_colors: list[int] = field(default_factory=[].copy)
    from_colors: list[int] = field(default_factory=[].copy)

    # the mail envelope and mail objects are essentially the same,
    # the mail object just has the message body.
    def read_mail(self) -> str:
        if self.msg_id < 0:
            raise InvalidMailIDError("Invalid message ID.")

        return self.account.read_mail(self.msg_id)


@dataclass
class APIMailList(AccountObject):
    mails: list[APIMailEnvelope] = field(default_factory=[].copy)


@dataclass
class PurchasableItem(AccountObject):
    item_type: PurchasableType
    item_id: int
    price: int

    def purchase(self) -> APICoinPurchaseResult:
        if self.account.account_id < 0:
            raise NotSignedInError("Cannot purchase items without an account.")

        return self.account.coin_purchase(self.item_type, self.item_id, self.price)


@dataclass
class APIPurchasePrices:
    current_coins: int
    coins: int
    clan_coins: int
    daily_free_skins: list[Skin]
    items: list[PurchasableItem]


@dataclass
class APIWheelOfNebulous(AccountObject):
    spin_type: SpinType
    spin_data: Any
    next_spin_ms: int
    spins_remaining: int

    def spin(self) -> APIWheelOfNebulous:
        if self.account.account_id < 0:
            raise NotSignedInError("Cannot spin without an account.")

        return self.account.get_spin_info(True)


@dataclass
class SignedInPlayer(APIPlayer):
    stats: APIPlayerStats
    profile: APIPlayerProfile

    def get_friends(self) -> list[APIFriend]:
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot fetch friends without an account.")

        return self.account.get_friends(include_friend_requests=False, include_friend_invites=False)

    def get_skins(self) -> list[APISkin]:
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot fetch skins without an account.")

        return self.account.get_skin_ids().skins

    def get_received_mail(self) -> APIMailList:
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot fetch mail without an account.")

        return self.account.get_mail(True)

    def get_sent_mail(self) -> APIMailList:
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot fetch mail without an account.")

        return self.account.get_mail(False)

    def send_mail(self, to: int, subject: str, message: str):
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot send mail without an account.")

        return self.account.send_mail(to, subject, message)

    def send_clan_mail(self, subject: str, message: str):
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot send mail without an account.")

        return self.account.send_mail(-1, subject, message, True, self.stats.clan_member.clan_role)

    def delete_sent_mail(self, msg_id: int):
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot delete mail without an account.")

        return self.account.delete_mail(msg_id, False)

    def delete_received_mail(self, msg_id: int):
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot delete mail without an account.")

        return self.account.delete_mail(msg_id, True)

    def get_skin_data(self, skin_id: int) -> bytes:
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot fetch skin data without an account.")

        return self.account.get_skin_data(skin_id).skin_data

    def checkin(self) -> APICheckinResult:
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot checkin without an account.")

        response = self.account.request_endpoint(Endpoints.CHECKIN, {})

        return APICheckinResult(
            response["CheckinReward"],
            response["RewardVideosRemaining"],
            response["Coins"],
        )

    def spin_wheel(self) -> APIWheelOfNebulous:
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot spin without an account.")

        return self.account.get_spin_info(True)

    @classmethod
    def from_account(cls, account: Account) -> SignedInPlayer:
        if account.account_id < 0:
            raise NotSignedInError("Cannot create player without a signed in account.")

        profile = account.get_player_profile(account.account_id)
        stats = account.get_player_stats(account.account_id)

        return cls(account, account.account_id, stats, profile)


@dataclass
class Ticket:
    ticket_str: str
    account_id: str = field(init=False)
    creation_date: str = field(init=False)
    signature: str = field(init=False)

    def __post_init__(self):
        if not self.ticket_str:
            self.account_id = ""
            self.creation_date = ""
            self.signature = ""

            return

        self.account_id = self.ticket_str.split(",")[0]
        self.creation_date = self.ticket_str.split(",")[1]
        self.signature = self.ticket_str.split(",")[2]


@dataclass
class Region:
    region_name: ServerRegions
    ip: str


class Account:
    API_URL: ClassVar[str] = "https://simplicialsoftware.com/api/account/"

    def __init__(self, ticket: str, region: ServerRegions, log_level: int = logging.INFO):
        self.ticket = Ticket(ticket)
        self.region = Region(region, "")
        self.logger = logging.getLogger("AccountAPI")

        logging.basicConfig(
            format="[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
            filename="account-api.log",
            filemode="w",
            encoding="utf-8",
            level=log_level,
        )

        self.logger.info("Logger initialized.")

        self.secure_bytes, self.region.ip = self.get_secure_ticket()

        if ticket != "":
            self.account_id = int(self.ticket.account_id)
            self.player_obj = SignedInPlayer.from_account(self)

            self.logger.info("Checking in...")
            self.player_obj.checkin()
        else:
            self.account_id = -1
            self.player_obj = None

        self.sale_info = self.get_sale_info()
        self.skin_url_base = self.get_skin_url_base()
        self.purchase_prices = self.get_purchase_prices(False)

        self.logger.info(f"Account ID: {self.account_id}")
        self.logger.info(f"Region: {self.region.region_name}")
        self.logger.info(f"Region IP: {self.region.ip}")

    @classmethod
    def no_account(cls, region: ServerRegions) -> Account:
        return cls("", region)

    def refresh(self):
        self.secure_bytes, self.region.ip = self.get_secure_ticket()

        self.logger.info("Refreshed secure ticket.")

    def get_region_ip(self) -> str:
        return self.region.ip

    def get_region(self) -> ServerRegions:
        return self.region.region_name

    def get_secure_ticket(self) -> tuple[bytes, str]:
        response = self.request_endpoint(Endpoints.SECURE_TICKET, {"region": str(self.region.region_name)})
        secure_ticket = response["RezPlEVBeW"]
        region_ip = response["IP"]
        secure_bytes = base64.b64decode(secure_ticket)

        return secure_bytes, region_ip

    def get_spin_info(self, spin: bool) -> APIWheelOfNebulous:
        response = self.request_endpoint(Endpoints.GET_SPIN_INFO, {"Spin": spin})

        return APIWheelOfNebulous(
            self,
            SpinType[response["SpinType"]],
            response["SpinData"],
            response["NextSpinRemainingMs"],
            response["SpinsRemaining"],
        )

    def get_skin_data(self, skin_id: int) -> APISkinData:
        response = self.request_endpoint(Endpoints.GET_SKIN_DATA, {"SkinID": skin_id})

        return APISkinData(CustomSkinStatus[response["SkinStatus"]], base64.b64decode(response["Data"]))

    def delete_mail(self, msg_id: int, received: bool):
        self.request_endpoint(Endpoints.DELETE_MAIL, {"MsgID": msg_id, "Received": received})

    def send_mail(
        self, to: int, subject: str, message: str, to_clan: bool = False, clan_role: ClanRole = ClanRole.INVALID
    ):
        data_map = {
            "ToAID": to,
            "Message": message,
            "Subject": subject,
            "ToAllClan": to_clan,
            "ClanRole": clan_role.name,
        }

        self.request_endpoint(Endpoints.SEND_MAIL, data_map)

    def get_purchase_prices(self, for_mail: bool) -> APIPurchasePrices:
        response = self.request_endpoint(Endpoints.GET_PURCHASE_PRICES, {"ForMail": for_mail})

        free_skins = [Skin(skin_id) for skin_id in response["DailyFreeSkins"]]

        items = []
        for item in response["Items"]:
            items.append(PurchasableItem(self, PurchasableType[item["ItemType"]], item["ItemID"], item["Price"]))

        return APIPurchasePrices(
            response["CurrentCoins"],
            response["Coins"],
            response["ClanCoins"],
            free_skins,
            items,
        )

    def coin_purchase(self, item_type: PurchasableType, item_id: int, price: int) -> APICoinPurchaseResult:
        data_map = {
            "ItemType": item_type.name,
            "ItemID": item_id,
        }

        if price > -1:
            data_map["ExpectedPrice"] = price

        response = self.request_endpoint(Endpoints.COIN_PURCHASE, data_map)

        return APICoinPurchaseResult(
            PurchasableType[response["ItemType"]],
            response["ItemID"],
            response["CoinsSpent"],
            response["Coins"],
            response["ClanCoins"],
        )

    def get_skin_url_base(self) -> APISkinURLBase:
        response = self.request_endpoint(Endpoints.GET_SKIN_URL_BASE, {})

        return APISkinURLBase(
            response["SkinURLBase"],
            response["UploadSizeLimitBytes"],
            response["UploadPetSizeLimitBytes"],
            response["ServerAddressOverrides"],
            response["ModAIDs"],
            response["YTAIDs"],
            response["FriendAIDs"],
            response["clanAllies"],
            response["clanEnemies"],
            response["freeTourneys"],
            response["freeArenas"],
            response["TutorialVYTID"],
            response["TutorialHYTID"],
            response["GameModeYTIDs"],
            GameMode[response["DoubleXPGameMode"]],
        )

    def get_sale_info(self) -> APISaleInfo:
        response = self.request_endpoint(Endpoints.GET_SALE_INFO, {})

        return APISaleInfo(
            response["ExpiresUtc"],
            response["NewTaco"],
            response["NewDiscord"],
            response["AnnouncementURL"],
            [SaleType(sale_type) for sale_type in response["SaleTypes"]],
        )

    def get_mail(self, received: bool) -> APIMailList:
        response = self.request_endpoint(Endpoints.GET_MAIL_LIST, {"Received": received})

        return APIMailList(
            self,
            [
                APIMailEnvelope(
                    self,
                    response["MsgID"],
                    response["FromAID"],
                    response["ToAID"],
                    response["ToName"],
                    response["FromName"],
                    response["Subject"],
                    response["isNew"],
                    response["TimeSent"],
                    response["TimeExpires"],
                    response["ToColors"],
                    response["FromColors"],
                )
                for response in response["Mails"]
            ],
        )

    def read_mail(self, msg_id: int) -> str:
        response = self.request_endpoint(Endpoints.READ_MAIL, {"MsgID": msg_id})

        return response["Message"]

    def get_skin_ids(self, skin_type: CustomSkinType = CustomSkinType.ALL) -> APISkinIDs:
        response = self.request_endpoint(Endpoints.GET_SKIN_IDS, {"Type": skin_type.name})

        skins = []
        for skin in response["Skins"]:
            skins.append(APISkin(skin["ID"], CustomSkinStatus[skin["Status"]], skin["PurchaseCount"]))

        return APISkinIDs(
            response["Coins"],
            response["ClanCoins"],
            response["purchasedSecondPet"],
            response["unlockedMultiskin"],
            response["skinMapPrice"],
            skins,
        )

    def get_friends(
        self,
        start_index: int = 0,
        include_friend_requests: bool = True,
        search: str = "",
        count: int = 100,
        include_friend_invites: bool = True,
    ) -> list[APIFriend]:
        response = self.request_endpoint(
            Endpoints.GET_FRIENDS,
            {
                "StartIndex": start_index,
                "IncludeFriendRequests": include_friend_requests,
                "Search": search,
                "Count": count,
                "IncludeFriendInvites": include_friend_invites,
            },
        )
        friends = []

        for friend in response["FriendRequests"]:
            friends.append(
                APIFriend(
                    self,
                    friend["Id"],
                    Relationship[friend["Relationship"]],
                    friend["BFF"],
                    friend["LastPlayedUtc"],
                )
            )

        return friends

    def get_player_profile(self, account_id: int) -> APIPlayerProfile:
        response = self.request_endpoint(
            Endpoints.GET_PLAYER_PROFILE,
            {
                "accountID": account_id,
            },
        )

        return APIPlayerProfile(
            response["profile"],
            response["customSkinID"],
            response["setNamePrice"],
            response["banned"],
            response["chatBanned"],
            response["arenaBanned"],
            Relationship[response["relationship"]],
            Font(response["profileFont"]),
            response["hasCommunitySkins"],
            response["hasCommunityPets"],
            response["hasCommunityParticles"],
            ProfileVisibility[response["profileVisibility"]],
            response["profileBGColorEnabled"],
            response["profileBGColor"],
            response["plasma"],
            response["yearsPlayed"],
            PlayerTitles(
                response["legend"],
                response["hero"],
                response["champion"],
                response["conqueror"],
                response["tricky"],
                response["supporter"],
                response["masterTamer"],
                response["tycoon"],
            ),
            response["views"],
            response["profileColors"],
            [Font(font_id) for font_id in response["profileFonts"]],
        )

    def get_player_stats(self, account_id: int) -> APIPlayerStats:
        response = self.request_endpoint(
            Endpoints.GET_PLAYER_STATS,
            {
                "AccountID": account_id,
            },
        )

        clan = Clan(response["ClanName"], response["ClanColors"], response["clanID"])

        special_objects = []
        for entry in response["SpecialObjects"]:
            # for some stupid reason, the api returns plural and inconsistent
            # names for the item types. thus, we must create a mapping to
            # convert the names to the correct enum.
            so2item_map = {
                "Beads": Item.BEAD,
                "Candies": Item.CANDY,
                "Drops": Item.RAINDROP,
                "Eggs": Item.EGG,
                "Leaves": Item.LEAF,
                "Moons": Item.MOON,
                "Nebulas": Item.NEBULA,
                "Notes": Item.NOTE,
                "Presents": Item.PRESENT,
                "Pumpkins": Item.PUMPKIN,
                "Snowflakes": Item.SNOWFLAKE,
                "Suns": Item.SUN,
            }

            special_objects.append({"Type": so2item_map[entry["Type"]], "Count": entry["Count"]})

        effective_clan_role = response["EffectiveClanRole"]
        if effective_clan_role is None:
            effective_clan_role = ClanRole.INVALID
        else:
            effective_clan_role = ClanRole[effective_clan_role]

        return APIPlayerStats(
            response["AccountID"],
            response["AccountName"],
            response["competitionBanned"],
            response["competitionBannedUntilMS"],
            response["chatBanned"],
            response["chatBannedUntilMS"],
            response["isSupporter"],
            response["DQ"],
            response["DQDone"],
            response["XPMultiplier"],
            response["XPMultiplierDurationRemainingS"],
            response["MassBoost"],
            response["MassBoostDurationS"],
            response["PlasmaBoost"],
            response["PlasmaBoostDurationRemainingS"],
            response["ClickType"],
            response["ClickDurationS"],
            response["LengthBoost"],
            response["LengthBoostDurationRemainingS"],
            response["PurchasedAliasColors"],
            response["PurchasedClanColors"],
            response["PurchasedBlobColor"],
            response["clickEnabled"],
            response["xpBoostEnabled"],
            response["massBoostEnabled"],
            response["CurrentCoins"],
            response["PurchasedSkinMap"],
            response["purchasedSecondPet"],
            response["unlockedMultiskin"],
            response["isAppleGuest"],
            clan,
            ClanMember(
                clan,
                response["CanStartClanWar"],
                response["CanJoinClanWar"],
                response["CanUploadClanSkin"],
                response["CanSetMOTD"],
                ClanRole[response["ClanRole"]],
                effective_clan_role,
                response["CanSelfPromote"],
            ),
            APIPlayerGeneralStats(
                response["XP"],
                response["DotsEaten"],
                response["BlobsEaten"],
                response["BlobsLost"],
                response["BiggestBlob"],
                response["MassGained"],
                response["MassEjected"],
                response["EjectCount"],
                response["SplitCount"],
                response["AverageScore"],
                response["HighestScore"],
                response["TimesRestarted"],
                response["LongestLifeMS"],
                response["GamesWon"],
                response["SMBHCollidedCount"],
                response["SMBHEatenCount"],
                response["BHCollidedCount"],
                response["ArenasWon"],
                response["CWsWon"],
                response["TBHCollidedCount"],
                response["TimesTeleported"],
                response["PowerupsUsed"],
                response["TrickCount"],
                response["MatchesWon"],
                response["ChallengesWon"],
                response["yearsPlayed"],
                response["Accolades"],
                response["MaxPlasmaChain"],
                response["CoinsCollected"],
                response["trianglesDestroyed"],
                response["squaresDestroyed"],
                response["pentagonsDestroyed"],
                response["hexagonsDestroyed"],
                response["playersKilled"],
                response["shotsFired"],
                response["damageDealt"],
                response["damageTaken"],
                response["damageHealed"],
                response["AchievementsEarned"],
                response["AchievementStats"],
                special_objects,
            ),
            response["AccountColors"],
            response["PurchasedAvatars"],
            response["PurchasedEjectSkins"],
            response["PurchasedHats"],
            response["PurchasedParticles"],
            response["PurchasedHalos"],
            response["PurchasedPets"],
            response["ValidCustomSkinIDs"],
            response["ValidCustomPetSkinIDs"],
            response["ValidCustomParticleIDs"],
            response["ClanColors"],
        )

    def request_endpoint(self, endpoint: Endpoints, data: dict) -> dict:
        url = f"{self.API_URL}{endpoint!s}"
        default_data = {
            "Game": constants.APP_NAME,
            "Version": constants.APP_VERSION,
            "Ticket": self.ticket.ticket_str,
        }

        default_data.update(data)
        self.logger.info(f"Requesting endpoint: {endpoint!s}")
        self.logger.info(f"Post Data: {default_data}")

        response = requests.post(url, data=default_data, timeout=10)

        if response.status_code != HTTPStatus.OK:
            raise Exception(f"Request failed with status code: {response.status_code}. Response: {response.text}")

        self.logger.info(f"Response[{response.status_code}]: {response.text}")

        return response.json()
