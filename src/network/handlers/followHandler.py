from utils import EventBUS

from events.twitch import EventFollow


class FollowHandler:

    async def dispatch(self, event):

        follow_evt = EventFollow(payload={
            "username": event.event.user_name,
        })

        await EventBUS.publish(follow_evt)