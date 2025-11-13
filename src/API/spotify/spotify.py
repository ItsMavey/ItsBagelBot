"""
Spotify API Wrapper

This module provides a simple wrapper for interacting with the Spotify API.
It includes all authentication and request handling functionalities towards the Spotify platform.

It also includes methods for playback, queue management, and searching tracks
with a custom ranking algorithm for fuzzy matching.
"""
from spotipy import Spotify, SpotifyException
from spotipy.oauth2 import SpotifyOAuth

from API.spotify import SpotifyHelper

from utils import settings, Logger


class SpotifyAPI:

    _logger = Logger('API.Spotify')

    def __init__(self):
        self.auth = SpotifyOAuth(
            client_id=settings.SPOTIFY['CLIENT_ID'],
            client_secret=settings.SPOTIFY['CLIENT_SECRET'],
            redirect_uri=settings.SPOTIFY['REDIRECT_URI'],
            scope="user-modify-playback-state user-read-playback-state playlist-modify-private"
        )

        self.helper = SpotifyHelper()

        self.refresh_token()

        self.spotify = Spotify(auth_manager=self.auth)



    def refresh_token(self, username: str = settings.MAIN_BROADCASTER):

        if not username or username.strip() == "":
            self._logger.warning("No username provided for Spotify token refresh.")
            return

        token = self.helper.get_refresh_token(username)

        if token:
            self.auth.refresh_access_token(token)
            self._logger.info("🔄 Retrieved Spotify refresh token.")

        token = self.auth.get_cached_token()

        if token:
            self.helper.save_refresh_token(username, token['refresh_token'])
            self._logger.info("✅ Saved Spotify refresh token.")

        else:
            self._logger.warning("No Spotify token available to refresh.")

    # %% --- Playback Controls ---

    def play(self):
        try:
            self.spotify.start_playback()

            return "Playback started."
        except SpotifyException as e:
            self._logger.error(f"[Spotify] Failed to start playback: {e}")
            return "Failed to start playback. Please ensure a device is active."

    def pause(self):
        try:
            self.spotify.pause_playback()

            return "Playback paused."
        except SpotifyException as e:
            self._logger.error(f"[Spotify] Failed to pause playback: {e}")
            return "Failed to stop playback. Please ensure a device is active."


    def next_track(self):
        try:
            self.spotify.next_track()

            return "Skipped to next track."
        except SpotifyException as e:
            self._logger.error(f"[Spotify] Failed to skip to next track: {e}")
            return "Failed to go skip song. Please ensure a device is active."


    def previous_track(self):
        try:
            self.spotify.previous_track()

            return "Went back to previous track."
        except SpotifyException as e:
            self._logger.error(f"[Spotify] Failed to go to previous track: {e}")
            return "Failed to go to previous song. Please ensure a device is active."

    def volume(self, volume_percent):
        try:
            self.spotify.volume(volume_percent)

            return "Volume set to {}%.".format(volume_percent)
        except SpotifyException as e:
            self._logger.error(f"[Spotify] Failed to set volume: {e}")
            return "Failed to start playback. Please ensure a device is active."


    def is_playing(self):
        try:
            state = self.spotify.current_playback()
            if not state:
                return None  # No active device
            return state.get("is_playing", False)
        except:
            return None

    # %% --- Queue Management ---

    def add_to_queue(self, track_uri, device_id=None):
        try:

            if device_id:
                self.spotify.add_to_queue(track_uri, device_id=device_id)
            else:
                self.spotify.add_to_queue(track_uri)
        except SpotifyException as e:
            self._logger.error(f"[Spotify] Failed to add track to queue: {e}")
            return "Failed to add track to queue. Please ensure a device is active."

    def search_to_queue(self, query):
        try:
            devices = self.spotify.devices()
            active_device = next((d for d in devices['devices'] if d['is_active']), None)
            if not active_device:
                return "No active device found. Please start playback on a Spotify device."
            device_id = active_device['id']

            results = self.spotify.search(q=query, type='track', limit=5)
            tracks = results['tracks']['items']

            if not tracks:
                return "No results found on Spotify."

            # Custom ranking algorithm for fuzzy matching
            ranked_tracks = sorted(tracks, key=lambda track: self._fuzzy_rank(track['name'], query), reverse=True)
            best_match = ranked_tracks[0]

            track_uri = best_match['uri']
            track_name = best_match['name']
            track_artist = best_match['artists'][0]['name']

            self.add_to_queue(track_uri, device_id=device_id)
            return f'Added {track_name} by {track_artist} to the queue.'

        except SpotifyException as e:
            print(f"[Spotify] Failed to search and add to queue: {e}")
            return "An error occurred while adding the song to the queue."

    def _fuzzy_rank(self, track_name, query):
        # Simple fuzzy ranking based on substring matching and length difference
        track_name_lower = track_name.lower()
        query_lower = query.lower()

        if query_lower in track_name_lower:
            return len(query_lower) / len(track_name_lower)  # Higher score for closer matches

        # Penalize based on length difference
        length_diff = abs(len(track_name_lower) - len(query_lower))
        return 1 / (1 + length_diff)
