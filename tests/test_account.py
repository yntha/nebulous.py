from dotenv import dotenv_values

from nebulous.game.account import Account, APIPlayer, ServerRegions

secrets = dotenv_values("../.env.secrets")


def test_fetch_other_player():
    account = Account.no_account(ServerRegions.US_EAST)
    player = APIPlayer.from_account_id(account, 4)

    print(f"Player: {player.account_name}")
    print(f"Level: {player.level}")
    print(f"Current XP: {player.stats.general_stats.xp}")

    clan_member = player.clan_member

    if clan_member is not None:
        print(f"Clan: {clan_member.clan.name}")
        print(f"Role: {clan_member.clan_role}")

    print(f"Account bio: {player.profile.bio}")


def test_fetch_self():
    account = Account(secrets.get("TICKET", ""), ServerRegions.US_EAST)  # type: ignore
    player = APIPlayer.from_account_id(account, account.account_id)

    print(f"Player: {player.account_name}")
    print(f"Level: {player.level}")
    print(f"Current XP: {player.stats.general_stats.xp}")

    clan_member = player.clan_member

    if clan_member is not None:
        print(f"Clan: {clan_member.clan.name}")
        print(f"Role: {clan_member.clan_role}")

    print(f"Account bio: {player.profile.bio}")

    # fetch friends
    print("Fetching friends...")

    friends = player.friends

    if len(friends) == 0:
        print("No friends :(")

        return

    for friend in friends:
        print(f"Friend: {friend.player.account_name}")
        print(f"Level: {friend.player.level}")
        print(f"Current XP: {friend.player.stats.general_stats.xp}")
        print(f"Account bio: {friend.player.profile.bio}")
        print(f"BFF: {friend.bff}")
        print(f"Last seen: {friend.last_played_utc}\n")
