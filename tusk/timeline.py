import time
import html2text
import requests


def timeline(instance_url: str, access_token: str):
    since_id = None
    request_url = f"https://{instance_url}/api/v1/timelines/home"
    while True:
        response = requests.get(
            url=f"{request_url}?since_id={since_id}" if since_id else request_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=60,
        )
        for post in reversed(response.json()):
            print(post["id"])
            print(post["account"]["display_name"])
            if spoiler_text := post["spoiler_text"]:
                print(f"[spoiler_text]: {spoiler_text}")
            h = html2text.HTML2Text()
            print(h.handle(post["content"]), end="")
            since_id = post["id"]

        # TODO: Define a constant for the refresh rate
        time.sleep(1)
