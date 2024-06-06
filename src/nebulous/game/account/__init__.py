from __future__ import annotations

import base64
from dataclasses import dataclass, field
from enum import StrEnum
from http import HTTPStatus
from typing import ClassVar

import requests

from nebulous.game import constants
from nebulous.game.enums import ClanRole, CustomSkinStatus, CustomSkinType, Font, Item, ProfileVisibility, Relationship
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
    GET_PLAYER_STATS = "GetPlayerStats"
    GET_SKIN_IDS = "GetSkinIDs"


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

    def __init__(self, ticket: str, region: ServerRegions):
        self.ticket = Ticket(ticket)
        self.region = Region(region, "")

        self.secure_bytes, self.region.ip = self.get_secure_ticket()

    def refresh(self):
        self.secure_bytes, self.region.ip = self.get_secure_ticket()

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
        response = self.request_endpoint(Endpoints.GET_SKIN_IDS, {
            "Type": skin_type.name
        })

        skins = []
        for skin in response["Skins"]:
            skins.append(
                APISkin(
                    skin["ID"],
                    CustomSkinStatus[skin["Status"]],
                    skin["PurchaseCount"]
                )
            )

        return APISkinIDs(
            response["Coins"],
            response["ClanCoins"],
            response["purchasedSecondPet"],
            response["unlockedMultiskin"],
            response["skinMapPrice"],
            skins
        )

    def get_player_profile(self, account_id: int) -> APIPlayerProfile:
        response = self.request_endpoint(Endpoints.GET_PLAYER_PROFILE, {
            "accountID": account_id,
        })

        return APIPlayerProfile(
            response["profile"],
            response["customSkinID"],
            response["setNamePrice"],
            response["banned"],
            response["chatBanned"],
            response["arenaBanned"],
            Relationship[response["relationship"]],
            Font[response["profileFont"]],
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
                response["tycoon"]
            ),
            response["views"],
            response["profileColors"],
            response["profileFonts"]
        )

    def get_player_stats(self, account_id: int) -> APIPlayerStats:
        response = self.request_endpoint(Endpoints.GET_PLAYER_STATS, {
            "AccountID": account_id,
        })

        clan = Clan(
                response["ClanName"],
                response["ClanColors"],
                response["clanID"]
        )

        special_objects = []
        for entry in response["SpecialObjects"]:
            special_objects.append({
                "Type": Item[entry["Type"]],
                "Count": entry["Count"]
            })

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
                ClanRole[response["EffectiveClanRole"]],
                response["CanSelfPromote"]
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
                special_objects
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
            response["ClanColors"]
        )

    def request_endpoint(self, endpoint: Endpoints, data: dict) -> dict:
        url = f"{self.API_URL}{endpoint!s}"
        default_data = {
            "Game": constants.APP_NAME,
            "Version": constants.APP_VERSION,
            "Ticket": self.ticket.ticket_str,
        }

        default_data.update(data)

        response = requests.post(url, data=default_data, timeout=10)

        if response.status_code != HTTPStatus.OK:
            raise Exception(f"Request failed with status code: {response.status_code}. Response: {response.text}")

        return response.json()
