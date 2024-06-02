import base64
from dataclasses import dataclass, field
from enum import StrEnum
from http import HTTPStatus

import requests

from nebulous.game import constants


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


@dataclass
class Ticket:
    ticket_str: str
    account_id: str = field(init=False)
    creation_date: str = field(init=False)
    signature: str = field(init=False)

    def __post_init__(self):
        self.account_id = self.ticket_str.split(",")[0]
        self.creation_date = self.ticket_str.split(",")[1]
        self.signature = self.ticket_str.split(",")[2]


@dataclass
class Region:
    region_name: ServerRegions
    ip: str


class Account:
    API_URL = "https://simplicialsoftware.com/api/account/"

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

    def request_endpoint(self, endpoint: Endpoints, data: dict) -> dict:
        url = f"{self.API_URL}{endpoint!s}"
        default_data = {
            "Game": constants.APP_NAME,
            "Version": constants.APP_VERSION,
            "Ticket": self.ticket.ticket_str,
        }

        default_data.update(data)

        response = requests.post(url, data=default_data)  # noqa: S113

        if response.status_code != HTTPStatus.OK:
            raise Exception(f"Request failed with status code: {response.status_code}. Response: {response.text}")

        return response.json()
