from commands import decorators as cmd
from commands.components import Component

from API import SPOTIFYAPI


class Spotify(Component):

    def __init__(self):
        self.component_name = "Spotify Commands"
        self.enabled = True


    @cmd.mod
    @cmd.command(name='togglesongrequests', aliases=['tsr'], description='Toggle song requests on/off', stream_status=True)
    async def toggle_song_requests(self, ctx):
        self.enabled = not self.enabled

        status = "enabled" if self.enabled else "disabled"
        return f"@{ctx.user} Song requests have been {status}."


    @cmd.command(name='songrequest', aliases=['sr'], description='Request a song to be played on stream via Spotify', stream_status=True)
    async def song_request(self, ctx):

        if not self.enabled:
            return f"@{ctx.user} Song requests are currently disabled."

        query =  ctx.message.strip()

        if not query or query == '':
            return f"@{ctx.user} Please provide a song name or artist to request."

        return SPOTIFYAPI.search_to_queue(query)

    @cmd.mod
    @cmd.command(name='skip', aliases=['next'], description='Skip the current song playing on stream', stream_status=True)
    async def skip(self, ctx):

        if not self.enabled:
            return f"@{ctx.user} Song requests are currently disabled."

        if not SPOTIFYAPI.is_playing():
            return f"@{ctx.user} No song is currently playing to skip."

        return SPOTIFYAPI.next_track()

    @cmd.mod
    @cmd.command(name='previous', aliases=['prev'], description='Play the previous song on Spotify', stream_status=True)
    async def previous(self, ctx):

        if not self.enabled:
            return f"@{ctx.user} Song requests are currently disabled."

        if not SPOTIFYAPI.is_playing():
            return f"@{ctx.user} No song is currently playing to go back to."

        return SPOTIFYAPI.previous_track()

    @cmd.mod
    @cmd.command(name='play', aliases=[], description='Resume playback on Spotify', stream_status=True)
    async def play(self, ctx):

        if not self.enabled:
            return f"@{ctx.user} Song requests are currently disabled."

        if SPOTIFYAPI.is_playing():
            return f"@{ctx.user} Spotify is already playing."

        return SPOTIFYAPI.play()

    @cmd.mod
    @cmd.command(name='pause', aliases=[], description='Pause playback on Spotify', stream_status=True)
    async def pause(self, ctx):

        if not self.enabled:
            return f"@{ctx.user} Song requests are currently disabled."

        if not SPOTIFYAPI.is_playing():
            return f"@{ctx.user} Spotify is already paused."

        return SPOTIFYAPI.pause()


    @cmd.mod
    @cmd.command(name='volume', aliases=['vol'], description='Set the volume on Spotify (0-100)', stream_status=True)
    async def volume(self, ctx):

        if not self.enabled:
            return f"@{ctx.user} Song requests are currently disabled."

        if not ctx.message or ctx.message.strip() == '':
            return f"@{ctx.user} Please provide a volume percentage (0-100)."

        try:
            volume_percent = int(ctx.message.strip())
        except ValueError:
            return f"@{ctx.user} Please provide a valid volume percentage (0-100)."

        if volume_percent < 0 or volume_percent > 100:
            return f"@{ctx.user} Volume must be between 0 and 100."

        return SPOTIFYAPI.volume(volume_percent)