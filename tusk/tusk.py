import argparse
import os
import pprint
import requests
import sys


def get_blocked_users(instance_url, access_token):
    response = requests.get(
        url=f"https://{instance_url}/api/v1/blocks?limit=10",
        headers={"Authorization": f"Bearer {access_token}"},
        data={},
    )
    print(f"{response.status_code=}")
    pprint.pprint(response.json())


def post(instance_url, access_token, body):
    response = requests.post(
        url=f"https://{instance_url}/api/v1/statuses",
        headers={"Authorization": f"Bearer {access_token}"},
        data={"status": body},
    )
    print(f"{response.status_code=}")
    pprint.pprint(response.json())


def parse(argv=sys.argv):

    usage = "tusk [COMMAND]"
    parser = argparse.ArgumentParser(usage=usage)

    # TODO: Add sub commands ex. tusk block list, tusk post --poll
    parser.add_argument("post", nargs="*", type=str, help="please type strings")
    parser.add_argument(
        "blocks", action="store_true", help="get the list of blocked users"
    )

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

    if args.blocks:
        get_blocked_users(instance_url, access_token)

    # FIXME: args.post = ["block"] if `tusk blocks `
    elif args.post:
        post(instance_url, access_token, " ".join(args.post[1:]))
