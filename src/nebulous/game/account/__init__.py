from __future__ import annotations

import base64
import logging
from dataclasses import dataclass, field
from enum import StrEnum
from http import HTTPStatus
from typing import ClassVar

import requests

from nebulous.game import constants
from nebulous.game.enums import ClanRole, CustomSkinStatus, CustomSkinType, Font, Item, ProfileVisibility, Relationship
from nebulous.game.exceptions import InvalidUserIDError, NotSignedInError
from nebulous.game.models.apiobjects import (
    APIPlayerGeneralStats,
    APIPlayerProfile,
    APIPlayerStats,
    APISkin,
    APISkinIDs,
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
    MAIL = "Mail"
    ADD_FRIEND = "AddFriend"
    GET_FRIENDS = "GetFriends"
    GET_PLAYER_STATS = "GetPlayerStats"
    GET_SKIN_IDS = "GetSkinIDs"


@dataclass
class APIPlayer:
    account: Account  # represents the current signed in account
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
        if account_id == -1:
            raise InvalidUserIDError("Invalid account ID.")

        return cls(account, account_id)


@dataclass
class APIFriend(APIPlayer):
    relationship: Relationship
    bff: bool
    last_played_utc: str


@dataclass
class SignedInPlayer(APIPlayer):
    def get_friends(self) -> list[APIFriend]:
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot fetch friends without an account.")

        return self.account.get_friends(include_friend_requests=False, include_friend_invites=False)

    def get_skins(self) -> list[APISkin]:
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot fetch skins without an account.")

        return self.account.get_skin_ids().skins

    @classmethod
    def from_account(cls, account: Account) -> SignedInPlayer:
        if account.account_id == -1:
            raise NotSignedInError("Cannot create player without a signed in account.")

        return cls(account, account.account_id)


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
        else:
            self.account_id = -1
            self.player_obj = None

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
