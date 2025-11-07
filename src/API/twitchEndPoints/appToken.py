import requests
from utils.settings import TWITCH


def get_app_token():
    """
    Get an App Access Token via Client Credentials Flow.
    Used for server-to-server requests.
    """
    url = "https://id.twitch.tv/oauth2/token"

    params = {
        "client_id": TWITCH["CLIENT_ID"],
        "client_secret": TWITCH["CLIENT_SECRET"],
        "grant_type": "client_credentials",
    }

    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()