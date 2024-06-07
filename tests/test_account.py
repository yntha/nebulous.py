import logging

from dotenv import dotenv_values

from nebulous.game.account import Account, APIPlayer, ServerRegions

secrets = dotenv_values(".env.secrets")
logger = logging.getLogger("Account API Tests")
logger.setLevel(logging.INFO)


def test_fetch_other_player():
    account = Account.no_account(ServerRegions.US_EAST)
    player = APIPlayer.from_account_id(account, 4)

    if player is None:
        logger.error("Player not found.")

        return

    logger.info(f"Player: {player.account_name}")
    logger.info(f"Level: {player.level}")
    logger.info(f"Current XP: {player.stats.general_stats.xp}")

    clan_member = player.clan_member

    if clan_member is not None:
        logger.info(f"Clan: {clan_member.clan.name}")
        logger.info(f"Role: {clan_member.clan_role}")

    logger.info(f"Account bio: {player.profile.bio}")


def test_fetch_self():
    account = Account(secrets.get("TICKET", ""), ServerRegions.US_EAST)  # type: ignore
    player = APIPlayer.from_account_id(account, account.account_id)

    if player is None:
        logger.error("Player not found.")

        return

    logger.info(f"Player: {player.account_name}")
    logger.info(f"Level: {player.level}")
    logger.info(f"Current XP: {player.stats.general_stats.xp}")

    clan_member = player.clan_member

    if clan_member is not None:
        logger.info(f"Clan: {clan_member.clan.name}")
        logger.info(f"Role: {clan_member.clan_role}")

    logger.info(f"Account bio: {player.profile.bio}")

    # fetch friends
    logger.info("Fetching friends...")

    friends = player.friends

    if len(friends) == 0:
        logger.info("No friends :(")

        return

    for friend in friends:
        if friend is None or friend.player is None:
            # this shouldn't be reached.
            logger.fatal("Error fetching friend.")

            continue

        logger.info(f"Friend: {friend.player.account_name}")
        logger.info(f"Level: {friend.player.level}")
        logger.info(f"Current XP: {friend.player.stats.general_stats.xp}")
        logger.info(f"Account bio: {friend.player.profile.bio}")
        logger.info(f"BFF: {friend.bff}")
        logger.info(f"Last seen: {friend.last_played_utc}\n")
