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
    APIAlerts,
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
    """
    Enum class representing the server regions available in the game.
    """

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
    GET_ALERTS = "GetAlerts"


@dataclass
class AccountObject:
    """
    Represents an account object.

    Attributes:
        account (Account): Represents the current signed-in account.
    """
    account: Account  # represents the current signed in account


@dataclass
class APIPlayer(AccountObject):
    """
    Represents a player in the game with an associated account ID.

    Attributes:
        account_id (int): The ID of the player's account.
    """

    account_id: int

    def get_profile(self) -> APIPlayerProfile:
        """
        Retrieves the player's profile.

        Returns:
            APIPlayerProfile: The player's profile.

        Raises:
            InvalidUserIDError: If the account ID is not valid.
        """
        if self.account_id < 0:
            raise InvalidUserIDError("Cannot fetch profile without a valid account ID.")

        return self.account.get_player_profile(self.account_id)

    def get_stats(self) -> APIPlayerStats:
        """
        Retrieves the player's stats.

        Returns:
            APIPlayerStats: The player's stats.

        Raises:
            InvalidUserIDError: If the account ID is not valid.
        """
        if self.account_id < 0:
            raise InvalidUserIDError("Cannot fetch stats without a valid account ID.")

        return self.account.get_player_stats(self.account_id)

    @classmethod
    def from_account_id(cls, account: Account, account_id: int) -> APIPlayer:
        """
        Creates an APIPlayer instance from an account ID.

        Args:
            account (Account): The account associated with the player.
            account_id (int): The ID of the player's account.

        Returns:
            APIPlayer: An instance of APIPlayer.

        Raises:
            InvalidUserIDError: If the account ID is not valid.
        """
        if account_id < 0:
            raise InvalidUserIDError("Invalid account ID.")

        return cls(account, account_id)


@dataclass
class APIFriend(APIPlayer):
    """
    Represents a friend in the game's account system.

    Attributes:
        relationship (Relationship): The relationship status with the friend.
        bff (bool): Indicates whether the friend is the user's best friend.
        last_played_utc (str): The last time the friend played the game in UTC format.
    """
    relationship: Relationship
    bff: bool
    last_played_utc: str


@dataclass
class APIMailEnvelope(AccountObject):
    """
    Represents a mail envelope in the game account.

    Attributes:
        msg_id (int): The ID of the mail message.
        from_aid (int): The ID of the sender account.
        to_aid (int): The ID of the recipient account.
        to_name (str): The name of the recipient.
        from_name (str): The name of the sender.
        subject (str): The subject of the mail.
        is_new (bool): Indicates whether the mail is new or not.
        time_sent (str): The time the mail was sent.
        time_expires (str): The time the mail expires.
        to_colors (list[int]): The colors associated with the recipient.
        from_colors (list[int]): The colors associated with the sender.
    """

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

    def read_mail(self) -> str:
        """
        Reads the content of the mail message.

        Returns:
            str: The message body of the mail.

        Raises:
            InvalidMailIDError: If the message ID is invalid.
        """
        if self.msg_id < 0:
            raise InvalidMailIDError("Invalid message ID.")

        return self.account.read_mail(self.msg_id)


@dataclass
class APIMailList(AccountObject):
    """A class representing a list of API mails for an account."""

    mails: list[APIMailEnvelope] = field(default_factory=[].copy)


@dataclass
class PurchasableItem(AccountObject):
    """
    Represents a purchasable item in the game.

    Attributes:
        item_type (PurchasableType): The type of the item.
        item_id (int): The ID of the item.
        price (int): The price of the item, in plasma.

    Methods:
        purchase() -> APICoinPurchaseResult:
            Purchase the item using the account's coins(plasma).
    """

    item_type: PurchasableType
    item_id: int
    price: int

    def purchase(self) -> APICoinPurchaseResult:
        """
        Purchase the item using the account's coins(plasma).

        Returns:
            APICoinPurchaseResult: The result of the purchase.

        Raises:
            NotSignedInError: If the account is not signed in.

        """
        if self.account.account_id < 0:
            raise NotSignedInError("Cannot purchase items without an account.")

        return self.account.coin_purchase(self.item_type, self.item_id, self.price)


@dataclass
class APIPurchasePrices:
    """
    Represents the purchase prices for various items in the game.

    Attributes:
        current_coins (int): The current number of coins(plasma).
        coins (int): The number of coins(plasma). (?)
        clan_coins (int): The number of clan coins(plasma).
        daily_free_skins (list[Skin]): A list of daily free skins.
        items (list[PurchasableItem]): A list of purchasable items.
    """
    current_coins: int
    coins: int
    clan_coins: int
    daily_free_skins: list[Skin]
    items: list[PurchasableItem]


@dataclass
class APIWheelOfNebulous(AccountObject):
    """
    Represents the API for the Wheel of Nebulous game.

    Attributes:
        spin_type (SpinType): The type of spin.
        spin_data (Any): Additional data related to the spin.
        next_spin_ms (int): The time in milliseconds until the next spin.
        spins_remaining (int): The number of spins remaining.

    Methods:
        spin() -> APIWheelOfNebulous: Spins the wheel and returns the updated APIWheelOfNebulous object.
    """

    spin_type: SpinType
    spin_data: Any
    next_spin_ms: int
    spins_remaining: int

    def spin(self) -> APIWheelOfNebulous:
        """
        Spins the wheel and returns the updated APIWheelOfNebulous object.

        Raises:
            NotSignedInError: If the account is not signed in.

        Returns:
            APIWheelOfNebulous: The updated APIWheelOfNebulous object.
        """
        if self.account.account_id < 0:
            raise NotSignedInError("Cannot spin without an account.")

        return self.account.get_spin_info(True)


@dataclass
class SignedInPlayer(APIPlayer):
    """
    Represents a signed-in player in the game.

    Attributes:
        stats (APIPlayerStats): The player's statistics.
        profile (APIPlayerProfile): The player's profile.

    Methods:
        get_friends(): Get the list of friends for the player.
        get_skins(): Get the list of skins owned by the player.
        get_received_mail(): Get the list of received mails for the player.
        get_sent_mail(): Get the list of sent mails by the player.
        send_mail(to, subject, message): Send a mail to another player.
        send_clan_mail(subject, message): Send a mail to the player's clan members.
        delete_sent_mail(msg_id): Delete a sent mail.
        delete_received_mail(msg_id): Delete a received mail.
        get_skin_data(skin_id): Get the data of a specific skin.
        checkin(): Perform a check-in action.
        spin_wheel(): Spin the wheel of Nebulous.
        from_account(account): Create a SignedInPlayer instance from an Account object.
    """

    stats: APIPlayerStats
    profile: APIPlayerProfile

    def get_friends(self) -> list[APIFriend]:
        """
        Get the list of friends for the player.

        Returns:
            list[APIFriend]: The list of friends.

        Raises:
            NotSignedInError: If the player is not signed in.
        """
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot fetch friends without an account.")

        return self.account.get_friends(include_friend_requests=False, include_friend_invites=False)

    def get_skins(self) -> list[APISkin]:
        """
        Get the list of skins owned by the player.

        Returns:
            list[APISkin]: The list of skins.

        Raises:
            NotSignedInError: If the player is not signed in.
        """
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot fetch skins without an account.")

        return self.account.get_skin_ids().skins

    def get_received_mail(self) -> APIMailList:
        """
        Get the list of received mails for the player.

        Returns:
            APIMailList: The list of received mails.

        Raises:
            NotSignedInError: If the player is not signed in.
        """
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot fetch mail without an account.")

        return self.account.get_mail(True)

    def get_sent_mail(self) -> APIMailList:
        """
        Get the list of sent mails by the player.

        Returns:
            APIMailList: The list of sent mails.

        Raises:
            NotSignedInError: If the player is not signed in.
        """
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot fetch mail without an account.")

        return self.account.get_mail(False)

    def send_mail(self, to: int, subject: str, message: str):
        """
        Send a mail to another player.

        Args:
            to (int): The recipient's account ID.
            subject (str): The subject of the mail.
            message (str): The content of the mail.

        Raises:
            NotSignedInError: If the player is not signed in.
        """
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot send mail without an account.")

        return self.account.send_mail(to, subject, message)

    def send_clan_mail(self, subject: str, message: str):
        """
        Send a mail to the player's clan members.

        Args:
            subject (str): The subject of the mail.
            message (str): The content of the mail.

        Raises:
            NotSignedInError: If the player is not signed in.
        """
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot send mail without an account.")

        return self.account.send_mail(-1, subject, message, True, self.stats.clan_member.clan_role)

    def delete_sent_mail(self, msg_id: int):
        """
        Delete a sent mail.

        Args:
            msg_id (int): The ID of the mail to delete.

        Raises:
            NotSignedInError: If the player is not signed in.
        """
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot delete mail without an account.")

        return self.account.delete_mail(msg_id, False)

    def delete_received_mail(self, msg_id: int):
        """
        Delete a received mail.

        Args:
            msg_id (int): The ID of the mail to delete.

        Raises:
            NotSignedInError: If the player is not signed in.
        """
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot delete mail without an account.")

        return self.account.delete_mail(msg_id, True)

    def get_skin_data(self, skin_id: int) -> bytes:
        """
        Get the data of a specific skin.

        Args:
            skin_id (int): The ID of the skin.

        Returns:
            bytes: The skin data.

        Raises:
            NotSignedInError: If the player is not signed in.
        """
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot fetch skin data without an account.")

        return self.account.get_skin_data(skin_id).skin_data

    def checkin(self) -> APICheckinResult:
        """
        Perform a check-in action.

        Returns:
            APICheckinResult: The result of the check-in action.

        Raises:
            NotSignedInError: If the player is not signed in.
        """
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot checkin without an account.")

        response = self.account.request_endpoint(Endpoints.CHECKIN, {})

        return APICheckinResult(
            response["CheckinReward"],
            response["RewardVideosRemaining"],
            response["Coins"],
        )

    def spin_wheel(self) -> APIWheelOfNebulous:
        """
        Spin the wheel of Nebulous.

        Returns:
            APIWheelOfNebulous: The result of spinning the wheel.

        Raises:
            NotSignedInError: If the player is not signed in.
        """
        if self.account is None or self.account.account_id < 0:
            raise NotSignedInError("Cannot spin without an account.")

        return self.account.get_spin_info(True)

    @classmethod
    def from_account(cls, account: Account) -> SignedInPlayer:
        """
        Create a SignedInPlayer instance from an Account object.

        Args:
            account (Account): The Account object.

        Returns:
            SignedInPlayer: The created SignedInPlayer instance.

        Raises:
            NotSignedInError: If the account is not signed in.
        """
        if account.account_id < 0:
            raise NotSignedInError("Cannot create player without a signed in account.")

        profile = account.get_player_profile(account.account_id)
        stats = account.get_player_stats(account.account_id)

        return cls(account, account.account_id, stats, profile)


@dataclass
class Ticket:
    """
    Represents a ticket object.

    Attributes:
        ticket_str (str): The string representation of the ticket.
        account_id (str): The account ID extracted from the ticket string.
        creation_date (str): The creation date extracted from the ticket string.
        signature (str): The signature extracted from the ticket string.
    """
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
    """
    Represents a game server region.

    Attributes:
        region_name (ServerRegions): The name of the region.
        ip (str): The IP address of the server in the region.
    """
    region_name: ServerRegions
    ip: str


class Account:
    """
    Represents a user account in the game.

    Attributes:
        API_URL (ClassVar[str]): The base URL for account operations.
        ticket (Ticket): The login ticket for the account.
        region (Region): The region to report to the account API.
        secure_bytes (bytes): The secure ticket in bytes.
        account_id (int): The ID of the account.
        player_obj (SignedInPlayer): The signed-in player object associated with the account.
        alerts (APIAlerts): Current pending alerts for the account.
        sale_info (APISaleInfo): Current sale information.
        skin_url_base (APISkinURLBase): The base URL for skin operations, among other things.
        purchase_prices (APIPurchasePrices): The current purchase prices for items in-game.

    Methods:
        __init__(self, ticket: str, region: ServerRegions, log_level: int = logging.INFO): Initializes an Account
            object.
        no_account(cls, region: ServerRegions) -> Account: Creates an Account object without a ticket.
        refresh(self): Refreshes the secure ticket.
        get_region_ip(self) -> str: Returns the server IP address of the region.
        get_region(self) -> ServerRegions: Returns the name of the region.
        get_secure_ticket(self) -> tuple[bytes, str]: Retrieves the secure ticket.
        get_alerts(self) -> APIAlerts: Retrieves the alerts for the account.
        get_spin_info(self, spin: bool) -> APIWheelOfNebulous: Retrieves spin information.
        get_skin_data(self, skin_id: int) -> APISkinData: Retrieves skin data.
        delete_mail(self, msg_id: int, received: bool): Deletes a mail.
        send_mail(self, to: int, subject: str, message: str, to_clan: bool = False,
            clan_role: ClanRole = ClanRole.INVALID): Sends a mail.
        get_purchase_prices(self, for_mail: bool) -> APIPurchasePrices: Retrieves purchase prices, in plasma.
        coin_purchase(self, item_type: PurchasableType, item_id: int, price: int) -> APICoinPurchaseResult: Performs a
            coin(plasma) purchase.
        get_skin_url_base(self) -> APISkinURLBase: Retrieves the skin URL base.
        get_sale_info(self) -> APISaleInfo: Retrieves sale information.
        get_mail(self, received: bool) -> APIMailList: Retrieves the list of mails.
        read_mail(self, msg_id: int) -> str: Reads a mail.
        get_skin_ids(self, skin_type: CustomSkinType = CustomSkinType.ALL) -> APISkinIDs: Retrieves skin IDs.
        get_friends(self, start_index: int = 0, include_friend_requests: bool = True, search: str = "",
            count: int = 100, include_friend_invites: bool = True) -> list[APIFriend]: Retrieves the list of friends.
    """
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
            self.alerts = self.get_alerts()

            self.logger.info("Checking in...")
            self.player_obj.checkin()
        else:
            self.account_id = -1
            self.player_obj = None
            self.alerts = None

        self.sale_info = self.get_sale_info()
        self.skin_url_base = self.get_skin_url_base()
        self.purchase_prices = self.get_purchase_prices(False)

        self.logger.info(f"Account ID: {self.account_id}")
        self.logger.info(f"Region: {self.region.region_name}")
        self.logger.info(f"Region IP: {self.region.ip}")

    @classmethod
    def no_account(cls, region: ServerRegions) -> Account:
        """
        Creates a new Account object with no account information.

        Args:
            cls (Account): The Account class.
            region (ServerRegions): The server region for the account.

        Returns:
            Account: A new Account object with no account information.
        """
        return cls("", region)

    def refresh(self):
        """
        Refreshes the secure ticket for the account.

        This method retrieves a new secure ticket and updates the `secure_bytes` and `region.ip` attributes of the
        account object.
        """
        self.secure_bytes, self.region.ip = self.get_secure_ticket()

        self.logger.info("Refreshed secure ticket.")

    def get_region_ip(self) -> str:
        """
        Returns the server IP address of the region associated with the account.

        Returns:
            str: The server IP address of the region.
        """
        return self.region.ip

    def get_region(self) -> ServerRegions:
        """
        Returns the region name of the server.

        Returns:
            ServerRegions: The region name of the server.
        """
        return self.region.region_name

    def get_secure_ticket(self) -> tuple[bytes, str]:
        """
        Retrieves a secure ticket and the corresponding region IP.

        Returns:
            A tuple containing the secure ticket as bytes and the region IP as a string.
        """
        response = self.request_endpoint(Endpoints.SECURE_TICKET, {"region": str(self.region.region_name)})
        secure_ticket = response["RezPlEVBeW"]
        region_ip = response["IP"]
        secure_bytes = base64.b64decode(secure_ticket)

        return secure_bytes, region_ip

    def get_alerts(self) -> APIAlerts:
        """
        Retrieves the pending alerts for the account.

        Returns:
            An instance of APIAlerts containing the account alerts.
        """
        response = self.request_endpoint(Endpoints.GET_ALERTS, {})

        return APIAlerts(
            response["HasFriendRequests"],
            response["HasClanInvites"],
            response["Coins"],
            response["MOTD"],
            response["ServerMessage"],
            response["NewMail"],
            response["BrandNewMail"],
            response["ServerMail"],
            response["birthday"],
            response["birthdayPlasma"],
            response["MassBoost"],
            response["MassBoostDurationS"],
            response["banReason"],
            response["BanUntilUtc"],
            response["competitionBanReason"],
            response["competitionBanUntilUtc"],
            response["chatBanReason"],
            response["chatBanUntilUtc"],
            response["massBoostEnabled"],
            ClanMember(
                Clan(
                    response["ClanName"],
                    response["ClanColors"],
                    response["clanID"],
                    response["ClanCoins"],
                ),
                False, False, False, False,
                response["ClanRole"],
                response["EffectiveClanRole"],
                response["CanSelfPromote"],
            )
        )

    def get_spin_info(self, spin: bool) -> APIWheelOfNebulous:
        """
        Retrieves spin information from the API.

        Args:
            spin (bool): Indicates whether to perform a spin or not.

        Returns:
            APIWheelOfNebulous: An instance of the APIWheelOfNebulous class containing the spin information.
        """
        response = self.request_endpoint(Endpoints.GET_SPIN_INFO, {"Spin": spin})

        return APIWheelOfNebulous(
            self,
            SpinType[response["SpinType"]],
            response["SpinData"],
            response["NextSpinRemainingMs"],
            response["SpinsRemaining"],
        )

    def get_skin_data(self, skin_id: int) -> APISkinData:
        """
        Retrieves the skin data for a given skin ID.

        Args:
            skin_id (int): The ID of the skin to retrieve data for.

        Returns:
            APISkinData: An instance of the APISkinData class containing the skin status and skin data.
        """
        response = self.request_endpoint(Endpoints.GET_SKIN_DATA, {"SkinID": skin_id})

        return APISkinData(CustomSkinStatus[response["SkinStatus"]], base64.b64decode(response["Data"]))

    def delete_mail(self, msg_id: int, received: bool):
        """
        Deletes a mail message.

        Args:
            msg_id (int): The ID of the mail message to delete.
            received (bool): Indicates if this is a received mail.
        """
        self.request_endpoint(Endpoints.DELETE_MAIL, {"MsgID": msg_id, "Received": received})

    def send_mail(
        self, to: int, subject: str, message: str, to_clan: bool = False, clan_role: ClanRole = ClanRole.INVALID
    ):
        """
        Sends a mail to the specified recipient.

        Args:
            to (int): The account ID of the recipient, or -1 for clan mail.
            subject (str): The subject of the mail.
            message (str): The content of the mail.
            to_clan (bool, optional): Indicates whether the mail should be sent to the entire clan. Defaults to False.
            clan_role (ClanRole, optional): The role of the player within the clan. Defaults to ClanRole.INVALID.
                Required if sending a clan mail.
        """
        data_map = {
            "ToAID": to,
            "Message": message,
            "Subject": subject,
            "ToAllClan": to_clan,
            "ClanRole": clan_role.name,
        }

        self.request_endpoint(Endpoints.SEND_MAIL, data_map)

    def get_purchase_prices(self, for_mail: bool) -> APIPurchasePrices:
        """
        Retrieves the purchase prices for items in the game, in plasma.

        Args:
            for_mail (bool): A boolean indicating whether the purchase prices are for mail.

        Returns:
            APIPurchasePrices: An instance of the APIPurchasePrices class containing the purchase prices in plasma.
        """
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
        """
        Purchase an item using coins(plasma).

        Args:
            item_type (PurchasableType): The type of the item to purchase.
            item_id (int): The ID of the item to purchase.
            price (int): The expected price of the item, in plasma.

        Returns:
            APICoinPurchaseResult: The result of the coin purchase operation.
        """
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
        """
        Retrieves the skin URL base from the API.

        Returns:
            APISkinURLBase: An instance of the APISkinURLBase class containing the skin URL base and other related
            information.
        """
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
        """
        Retrieves the sale information from the API.

        Returns:
            APISaleInfo: An object containing the sale information, including the expiration date,
            new Taco YouTube URL, new Discord invite URL, announcement URL, and sale types.
        """
        response = self.request_endpoint(Endpoints.GET_SALE_INFO, {})

        return APISaleInfo(
            response["ExpiresUtc"],
            response["NewTaco"],
            response["NewDiscord"],
            response["AnnouncementURL"],
            [SaleType(sale_type) for sale_type in response["SaleTypes"]],
        )

    def get_mail(self, received: bool) -> APIMailList:
        """
        Retrieves the list of mails based on the received flag.

        Args:
            received (bool): Flag indicating whether to retrieve received mails (True) or sent mails (False).

        Returns:
            APIMailList: An instance of APIMailList containing the retrieved mails.
        """
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
        """
        Reads a mail message with the given message ID.

        Args:
            msg_id (int): The ID of the mail message to read.

        Returns:
            str: The content of the mail message.
        """
        response = self.request_endpoint(Endpoints.READ_MAIL, {"MsgID": msg_id})

        return response["Message"]

    def get_skin_ids(self, skin_type: CustomSkinType = CustomSkinType.ALL) -> APISkinIDs:
        """
        Retrieves the skin IDs for the specified skin type.

        Args:
            skin_type (CustomSkinType, optional): The type of skin to retrieve IDs for. Defaults to CustomSkinType.ALL.

        Returns:
            APISkinIDs: An object containing the skin IDs and other related information.
        """
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
        """
        Retrieves a list of friends for the account.

        Args:
            start_index (int, optional): The starting index for the list of friends. Defaults to 0.
            include_friend_requests (bool, optional): Whether to include friend requests in the list. Defaults to True.
            search (str, optional): A search string to filter the friends. Defaults to an empty string.
            count (int, optional): The maximum number of friends to retrieve. Defaults to 100.
            include_friend_invites (bool, optional): Whether to include friend invites in the list. Defaults to True.

        Returns:
            list[APIFriend]: A list of APIFriend objects representing the friends.
        """
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
        """
        Retrieves the player profile for the specified account ID.

        Args:
            account_id (int): The ID of the account.

        Returns:
            APIPlayerProfile: An instance of the APIPlayerProfile class representing the player profile.
        """
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
        """
        Retrieves the player statistics for the given account ID.

        Args:
            account_id (int): The ID of the account.

        Returns:
            APIPlayerStats: The player statistics for the account.
        """
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
        """
        Sends a request to the specified endpoint with the provided data.

        Args:
            endpoint (Endpoints): The endpoint to send the request to.
            data (dict): Additional POST data to include in the request.

        Returns:
            dict: The JSON response from the server.

        Raises:
            Exception: If the request fails with a non-OK status code.
        """
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
