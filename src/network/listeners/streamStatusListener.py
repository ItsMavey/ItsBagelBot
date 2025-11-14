from network.handlers import StreamStatusHandler

from utils import Logger

class StreamStatusListener:

    _logger = Logger('System.Network.Listener')

    def __init__(self):
        self.handler = StreamStatusHandler()

    async def register(self, eventsub, broadcaster_id, bot_id):
        # Register online/offline event callbacks
        await eventsub.listen_stream_online(
            broadcaster_user_id=broadcaster_id,
            callback=self.handler.dispatch_live,
        )

        await eventsub.listen_stream_offline(
            broadcaster_user_id=broadcaster_id,
            callback=self.handler.dispatch_offline,
        )

        self._logger.info("🔴 Registered: channel.stream_status")