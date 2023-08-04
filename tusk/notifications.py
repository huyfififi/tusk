import time
import requests

import html2text

from .constants import NOTIFICATION_REFRESH_RATE


__all__ = ["notifications"]


def notifications(instance_url: str, access_token: str) -> None:
    since_id = None
    request_url = f"https://{instance_url}/api/v1/notifications"
    while True:
        response = requests.get(
            url=f"{request_url}?since_id={since_id}" if since_id else request_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=60,
        )
        for notification in reversed(response.json()):
            print(notification["account"]["display_name"])
            print(notification["type"])
            if notification["type"] == "follow":
                print()
            else:
                print(notification["status"]["account"]["display_name"])
                print(html2text.html2text(notification["status"]["content"]), end="")
        time.sleep(NOTIFICATION_REFRESH_RATE)
