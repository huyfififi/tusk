import argparse
import os
import pprint
import requests
import sys


def post(instance_url, access_token, body):
    response = requests.post(
        url=f"https://{instance_url}/api/v1/statuses",
        headers={"Authorization": f"Bearer {access_token}"},
        data={"status": body},
    )
    print(response.status_code)
    if response.status_code == 200:
        pprint.pprint(response.json())


def parse(argv=sys.argv):

    usage = "tusk [COMMAND]"
    parser = argparse.ArgumentParser(usage=usage)

    parser.add_argument("post", nargs="*", type=str, help="please type strings")

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

    if args.post:
        post(instance_url, access_token, " ".join(args.post[1:]))
