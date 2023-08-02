import requests

import html2text


__all__ = ["delete", "favorite", "post"]


def delete(instance_url: str, access_token: str, status_id: str) -> None:
    response = requests.delete(
        url=f"https://{instance_url}/api/v1/statuses/{status_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=60,
    )
    print("Successfully deleted the status.")
    response_data = response.json()
    print(response_data["id"])
    print(response_data["account"]["display_name"])
    print(html2text.html2text(response_data["text"]), end="")


def favorite(instance_url: str, access_token: str, status_id: str) -> None:
    response = requests.post(
        url=f"https://{instance_url}/api/v1/statuses/{status_id}/favourite",  # UK English
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=60,
    )
    # TODO: deal with 401 and 404
    print("Successfully favorited the status.")
    response_data = response.json()
    print(response_data["id"])
    print(response_data["account"]["display_name"])
    print(html2text.html2text(response_data["content"]), end="")


def post(instance_url, access_token, body, args):
    response = requests.post(
        url=f"https://{instance_url}/api/v1/statuses",
        headers={"Authorization": f"Bearer {access_token}"},
        data={"status": body},
        timeout=60,
    )
    print("Successfully posted the status.")
    response_data = response.json()
    print(response_data["id"])
    print(response_data["account"]["display_name"])
    print(html2text.html2text(response_data["content"]), end="")
