from dataclasses import dataclass
from typing import Literal
from events.Event import BaseEvent

from events.twitch.payloads import ChatMessagePayload, ChatCommandPayload



@dataclass
class EventChatMessage(BaseEvent):
    name: Literal["twitch.chat.message"] = "twitch.chat.message"
    source: Literal["twitch"] = "twitch"
    payload: ChatMessagePayload = None


@dataclass
class EventChatCommand(BaseEvent):
    name: Literal["twitch.chat.command"] = "twitch.chat.command"
    source: Literal["twitch"] = "twitch"
    payload: ChatCommandPayload = None
