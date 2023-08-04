import argparse
import os
import pprint
import requests
import sys
import time
from typing import List

import html2text

# from .timeline import timeline
from .utils import filter_dict


# Mastodon's API rate limits per user account. By default, the limit is 300 requests per 5 minute time slot.
# 300 // 5 // 60 = 1 request per second
TIMELINE_REFRESH_RATE = 5  # in seconds
NOTIFICATION_REFRESH_RATE = 15


class EnvNotSet(Exception):
    pass


class Endpoint:
    BLOCK = "api/v1/blocks"
    NOTIFICATIONS = "api/v1/notifications"
    STATUSES = "api/v1/statuses"
    TIMELINE_HOME = "api/v1/timelines/home"


class Handler:
    def __init__(self) -> None:
        self.domain = os.getenv("MASTODON_INSTANCE_DOMAIN")
        self.access_token = os.getenv("MASTODON_ACCESS_TOKEN")
        if not self.domain:
            raise EnvNotSet(
                "`MASTODON_INSTANCE_DOMAIN` is not set in env. Please provide a value and try again."
            )
        if not self.access_token:
            raise EnvNotSet(
                "`MASTODON_ACCESS_TOKEN` is not set in env. Please provide a value and try again."
            )

        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def block(self, args) -> None:
        def list_blocked_users():
            # TODO: Support paginatio
            # This command only shows 40 users maximumn
            DISPLAY_FIELDS = ("acct", "display_name", "note")
            request_url = f"https://{self.domain}/{Endpoint.BLOCK}"
            response = requests.get(
                url=request_url,
                headers=self.headers,
                timeout=60,
            )
            blocked_users = response.json()
            for blocked_user in blocked_users:
                pprint.pprint(filter_dict(blocked_user, DISPLAY_FIELDS), indent=2)

        if args.list:
            list_blocked_users()

    def notifications(self) -> None:
        # Stream notifications
        request_url = f"https://{self.domain}/{Endpoint.NOTIFICATIONS}"
        since_id = None
        while True:
            response = requests.get(
                url=f"{request_url}?since_id={since_id}" if since_id else request_url,
                headers=self.headers,
                timeout=60,
            )
            for notification in reversed(response.json()):
                print(
                    notification["account"]["display_name"]
                    or notification["account"]["acct"]
                )
                print(notification["type"])
                if notification["type"] == "follow":
                    print()
                else:
                    print(
                        notification["status"]["account"]["display_name"]
                        or notification["status"]["account"]["acct"]
                    )
                    print(
                        html2text.html2text(notification["status"]["content"]), end=""
                    )
            time.sleep(NOTIFICATION_REFRESH_RATE)

    def delete(self, status_id: str) -> None:
        response = requests.delete(
            url=f"https://{self.domain}/{Endpoint.STATUSES}/{status_id}",
            headers=self.headers,
            timeout=60,
        )
        response_data = response.json()
        if response.status_code == 200:
            print("Successfully deleted the status.")
            print(response_data["id"])
            print(
                response_data["account"]["display_name"]
                or response_data["account"]["acct"]
            )
            print(html2text.html2text(response_data["text"]), end="")
        else:
            # 401 or 404
            print(response.status_code)
            print(response_data)

    def favorite(self, status_id: str) -> None:
        response = requests.post(
            url=f"https://{self.domain}/{Endpoint.STATUSES}/{status_id}/favourite",
            headers=self.headers,
            timeout=60,
        )
        response_data = response.json()
        if response.status_code == 200:
            print("Successfully favourited the status.")
            print(response_data["id"])
            print(
                response_data["account"]["display_name"]
                or response_data["account"]["acct"]
            )
            print(html2text.html2text(response_data["content"]), end="")
        else:
            # 401 or 404
            print(response.status_code)
            print(response_data)

    def post(self, content: List[str]) -> None:
        response = requests.post(
            url=f"https://{self.domain}/{Endpoint.STATUSES}",
            headers=self.headers,
            data={"status": " ".join(content)},
            timeout=60,
        )
        response_data = response.json()
        if response.status_code == 200:
            print("Successfully posted a status.")
            print(response_data["id"])
            print(
                response_data["account"]["display_name"]
                or response_data["account"]["acct"]
            )
            print(html2text.html2text(response_data["content"]), end="")
        else:
            # 401 or 422
            print(response.status_code)
            print(response_data)

    def timeline(self) -> None:
        since_id = None
        request_url = f"https://{self.domain}/{Endpoint.TIMELINE_HOME}"
        while True:
            response = requests.get(
                url=f"{request_url}?since_id={since_id}" if since_id else request_url,
                headers=self.headers,
                timeout=60,
            )

            if response.status_code == 200:
                for post in reversed(response.json()):
                    print(post["id"])
                    print(post["account"]["display_name"])
                    if spoiler_text := post["spoiler_text"]:
                        print(f"[spoiler_text]: {spoiler_text}")
                    if post["media_attachments"]:
                        print(
                            f"[media]: {[media['id'] for media in post['media_attachments']]}"
                        )
                    print(html2text.html2text(post["content"]), end="")
                    since_id = post["id"]

                time.sleep(TIMELINE_REFRESH_RATE)

            else:
                # 401
                print(f"{response.status_code=}")
                print(f"{response.text=}")


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
    handler = Handler()
    args = parse()

    if args.subcommand == "block":
        handler.block(args)
    elif args.subcommand == "notifications":
        handler.notifications()

    elif args.subcommand == "favorite":
        handler.favorite(args.status_id)

    elif args.subcommand == "delete":
        handler.delete(args.status_id)

    elif args.subcommand == "post":
        handler.post(args.content)

    elif args.subcommand == "timeline":
        handler.timeline()
