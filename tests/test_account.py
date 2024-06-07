import logging
import time

from dotenv import dotenv_values

from nebulous.game.account import Account, APIPlayer, ServerRegions
from nebulous.game.natives import xp2level

secrets = dotenv_values(".env.secrets")
logger = logging.getLogger("Account API Tests")
logger.setLevel(logging.INFO)


def test_fetch_other_player():
    account = Account.no_account(ServerRegions.US_EAST)
    player = APIPlayer.from_account_id(account, 4)
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


def test_fetch_self():
    account = Account(secrets.get("TICKET", ""), ServerRegions.US_EAST)  # type: ignore
    player = account.player_obj

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
