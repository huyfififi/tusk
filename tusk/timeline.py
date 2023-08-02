import time
import html2text
import requests

from .constants import REFRESH_RATE


def timeline(instance_url: str, access_token: str) -> None:
    since_id = None
    request_url = f"https://{instance_url}/api/v1/timelines/home"
    while True:
        response = requests.get(
            url=f"{request_url}?since_id={since_id}" if since_id else request_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=60,
        )

        if response.status_code == 429:
            print(f"{response.status_code=}")
            print(f"{response.json()}=")  # {'error': 'Too many requests'}

        elif response.status_code == 200:
            for post in reversed(response.json()):
                print(post["id"])
                print(post["account"]["display_name"])
                if spoiler_text := post["spoiler_text"]:
                    print(f"[spoiler_text]: {spoiler_text}")
                if post["media_attachments"]:
                    print(f"[media]: {post['media_attachments']['id']}")
                h = html2text.HTML2Text()
                print(h.handle(post["content"]), end="")
                since_id = post["id"]

            time.sleep(REFRESH_RATE)

        else:
            print(f"{response.status_code=}")
            print(f"{response.text=}")
            print("Unknown error occurred. Quitting timeline view.")
            return
