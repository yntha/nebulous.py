# nebulous.py

[![PyPI - Version](https://img.shields.io/pypi/v/nebulous.py.svg)](https://pypi.org/project/nebulous.py)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nebulous.py.svg)](https://pypi.org/project/nebulous.py)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)
- [Usage](#usage)
    - [Utilizing the client](#utilizing-the-client)
    - [Interacting with the API](#interacting-with-the-api)
    - [Dumping Packets](#dumping-packets)

## Installation
1. Install [git](https://git-scm.com/downloads)
2. Install [`java-random`](https://github.com/MostAwesomeDude/java-random): `python -m pip install --user git+https://github.com/MostAwesomeDude/java-random`
    - NOTE: This is a required step, as the `java-random` package on pypi is outdated and broken.
3. Install `nebulous.py`: `python -m pip install --user nebulous.py`

## Usage
### Utilizing the client
```python
import asyncio
import logging

from dotenv import dotenv_values

from nebulous.game.account import ServerRegions
from nebulous.game.models.client import Client, ClientCallbacks
from nebulous.game.models.gameobjects import GamePlayer
from nebulous.game.packets import ConnectRequest3, ConnectResult2, Disconnect, GameData, KeepAlive

secrets = dotenv_values("../.env.secrets")
logger = logging.getLogger("Client Tests")
logger.setLevel(logging.INFO)


class TestCallbacks(ClientCallbacks):
    async def on_connect(self, client: Client, packet: ConnectRequest3) -> ConnectRequest3:
        print("Connected to server")
        return packet

    async def on_disconnect(self, client: Client, packet: Disconnect) -> Disconnect:
        print("Disconnected from server")
        return packet

    async def on_keep_alive(self, client: Client, packet: KeepAlive) -> KeepAlive:
        print("Sending keep alive packet")
        return packet

    async def on_connect_result(self, client: Client, packet: ConnectResult2) -> ConnectResult2:
        print(f"Received connection result: {packet.result}")
        return packet

    async def on_game_data(self, client: Client, packet: GameData) -> GameData:
        print(f"Received game data")
        return packet

    async def on_player_ready(self, client: Client, player: GamePlayer) -> GamePlayer:
        print(f"Player ready: {player.name}, index: {player.index}")

        await client.chat.send_game_message("Hello, world! :)")

        return player


async def test_client():
    client = Client(secrets.get("TICKET", ""), ServerRegions.US_EAST, callbacks=TestCallbacks())  # type: ignore

    await client.start()


if __name__ == "__main__":
    asyncio.run(test_client())
```

### Interacting with the API
Note: Upon signing in, the api client will perform a series of requests to fetch the player's data, among other things(e.g. sale info, purchase prices, etc.). This also includes an automatic account check-in, which grants 50 plasma each day.

From [`test_account.py`](tests/test_account.py):
```python
def test_fetch_self():
    account = Account(secrets.get("TICKET", ""), ServerRegions.US_EAST)  # type: ignore
    player = account.player_obj

    if player is None:
        logger.error("Failed to fetch player object")

        return

    player_profile = player.get_profile()
    player_stats = player.get_stats()

    player_xp = player_stats.general_stats.xp

    logger.info(f"Player: {player_stats.account_name}")
    logger.info(f"Level: {xp2level(player_xp)}")
    logger.info(f"Current XP: {player_xp}")

    clan_member = player_stats.clan_member

    logger.info(f"Clan: {clan_member.clan.name}")
    logger.info(f"Role: {clan_member.clan_role}")

    logger.info(f"Account bio: {player_profile.bio}")

    # fetch friends
    logger.info("Fetching friends...")

    friends = player.get_friends()

    if len(friends) == 0:
        logger.info("No friends :(")

        return

    for friend in friends:
        friend_profile = friend.get_profile()
        friend_stats = friend.get_stats()
        friend_xp = friend_stats.general_stats.xp

        logger.info(f"Friend: {friend_stats.account_name}")
        logger.info(f"Level: {xp2level(friend_xp)}")
        logger.info(f"Current XP: {friend_xp}")
        logger.info(f"Account bio: {friend_profile.bio}")
        logger.info(f"BFF: {friend.bff}")
        logger.info(f"Last seen: {friend.last_played_utc}\n")

        logger.info("Cooldown for 1.5 seconds...")
        time.sleep(1.5)  # don't spam the API
```

`Client` objects also contain an instance to an `Account` object, which can be accessed via `client.account`.

### Dumping Packets
You can also dump packets as json, as shown in [`sample_packet.json`](sample_packet.json):
```python
print(packet.as_json(indent=4))
```

## License

`nebulous.py` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
