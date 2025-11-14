from typing_extensions import override

from utils import EventBUS

from events.twitch import EventChatMessage, EventChatCommand
from events.twitch.payloads import ChatMessagePayload, ChatCommandPayload

from payload import Permission

from network.handlers import BaseHandler

class ChatHandler(BaseHandler):

    def event_parser(self, event):
        badges = {b.set_id for b in event.event.badges}

        is_mod = 'moderator' in badges
        is_vip = 'vip' in badges
        is_sub = 'subscriber' in badges

        msg = event.event.message.text
        username = event.event.chatter_user_name
        user_id = event.event.chatter_user_id

        broadcaster_id = event.event.broadcaster_user_id

        return username, user_id, broadcaster_id, msg, is_mod, is_vip, is_sub

    async def dispatch(self, event):
        username, user_id, broadcaster_id, msg, is_mod, is_vip, is_sub = self.event_parser(event)

        if msg.startswith('!'):
            cmd_evt = EventChatCommand(payload=
                ChatCommandPayload(
                    username= username,
                    command = msg,
                    user_id = user_id,
                    permission = Permission(
                        is_broadcaster = (user_id == broadcaster_id),
                        is_mod = is_mod,
                        is_vip = is_vip,
                        is_subscriber = is_sub
                    )
                ))
            await EventBUS.publish(cmd_evt)


        chat_evt = EventChatMessage(payload=
            ChatMessagePayload(
                username= username,
                message = msg,
                user_id = user_id,
                is_mod = is_mod,
                is_vip = is_vip,
                is_subscriber = is_sub
            ))


        await EventBUS.publish(chat_evt)


