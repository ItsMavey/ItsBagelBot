from database.models import APITokens as Tokens

from utils import Logger


class SpotifyHelper:

    _logger = Logger("API.Spotify.Helper")


    def save_refresh_token(self, username: str, refresh_token: str):
        """Save or update a Spotify refresh token for a given username."""
        username = username.lower()
        token = Tokens.get_token("spotify_refresh_token", username)

        if token is None:
            Tokens.create(
                name="spotify_refresh_token",
                streamer_name=username,
                refresh_token=refresh_token
            )
            self._logger.info(f"🆕 Saved new Spotify refresh token for user: {username}")
        else:
            token.refresh_token = refresh_token
            token.save()
            self._logger.info(f"🔁 Updated Spotify refresh token for user: {username}")

    def get_refresh_token(self, username: str):
        """Retrieve a stored Spotify refresh token for a given username."""
        username = username.lower()
        token = Tokens.get_token("spotify_refresh_token", username)

        if token is None:
            self._logger.warning(f"No Spotify refresh token found for user: {username}")
            return None

        return token.refresh_token
