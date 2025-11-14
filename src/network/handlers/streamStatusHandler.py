from utils import EventBUS

from events.twitch import EventStreamOnline, EventStreamOffline

from payload import Permission

from network.handlers import BaseHandler

class StreamStatusHandler(BaseHandler):


    async def dispatch_live(self, event):
        evt = EventStreamOnline(payload=
            {
                "title": event.event.title,
                "category": event.event.game_id,
                "started_at": event.event.started_at
            }
        )
        await EventBUS.publish(evt)

    async def dispatch_offline(self, event):
        evt = EventStreamOffline(payload=
            {
                "ended_at": event.event.ended_at
            }
        )
        await EventBUS.publish(evt)