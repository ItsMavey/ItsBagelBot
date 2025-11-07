from API.spotify import SpotifyAPI
from API.twitch import TwitchAPI

from utils.settings import MAIN_BROADCASTER


TWITCHAPI = TwitchAPI(MAIN_BROADCASTER)

SPOTIFYAPI = SpotifyAPI()

from API.helix import Helix

HELIX = Helix()