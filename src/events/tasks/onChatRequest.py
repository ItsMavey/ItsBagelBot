from dataclasses import dataclass
from typing import Literal
from events.Event import BaseEvent

from events.tasks.payloads import ChatRequestPayload



@dataclass
class EventChatRequest(BaseEvent):
    name: Literal["twitch.chat.message"] = "bot.chat.request"
    source: Literal["twitch"] = "bot"
    payload: ChatRequestPayload = None