import argparse
import os
import pprint
import requests
import sys

from .statuses import post, favorite, delete
from .timeline import timeline
from .notifications import notifications
from .utils import filter_dict


def block(instance_url, access_token, args):
    if not args.list:
        # other operations are not supported at the moment.
        return

    DISPLAY_FIELDS = ("acct", "display_name", "note")

    response = requests.get(
        url=f"https://{instance_url}/api/v1/blocks?limit=10",
        headers={"Authorization": f"Bearer {access_token}"},
        data={},
        timeout=60,
    )
    blocked_users = response.json()
    for blocked_user in blocked_users:
        pprint.pprint(filter_dict(blocked_user, keys=DISPLAY_FIELDS), indent=2)


def parse(argv=sys.argv):
    usage = "tusk [COMMAND]"
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("-g", "--global")

    subparsers = parser.add_subparsers(dest="subcommand")
    post_parser = subparsers.add_parser("post")
    post_parser.add_argument(dest="content", nargs="*", type=str, help="Post strings.")

    block_parser = subparsers.add_parser("block")
    block_parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="Retrieve the list of blocked users.",
    )

    subparsers.add_parser("timeline")

    favorite_parser = subparsers.add_parser("favorite")
    favorite_parser.add_argument(
        dest="status_id", nargs="?", type=str, help="Favorite a status."
    )

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument(
        dest="status_id", nargs="?", type=str, help="Delete a status."
    )

    subparsers.add_parser("notifications")

    args = parser.parse_args()
    return args


def main():
    access_token = os.getenv("MASTODON_ACCESS_TOKEN")
    if not access_token:
        print("Could not read access token from env")
        return

    instance_url = os.getenv("MASTODON_INSTANCE_URL")
    if not instance_url:
        print("Could not read instance URL from env")
        return

    args = parse()

    if args.subcommand == "block":
        block(instance_url, access_token, args)

    elif args.subcommand == "post":
        post(instance_url, access_token, " ".join(args.content), args)

    elif args.subcommand == "timeline":
        timeline(instance_url, access_token)

    elif args.subcommand == "favorite":
        favorite(instance_url, access_token, args.status_id)

    elif args.subcommand == "delete":
        delete(instance_url, access_token, args.status_id)

    elif args.subcommand == "notifications":
        notifications(instance_url, access_token)
