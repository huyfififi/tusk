import requests

import html2text


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
