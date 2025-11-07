from utils import EventBUS

from events.twitch import EventChatMessage, EventChatCommand
from events.twitch.payloads import ChatMessagePayload, ChatCommandPayload

from payload import Permission

from network.handlers import BaseHandler

class ChatHandler(BaseHandler):
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


