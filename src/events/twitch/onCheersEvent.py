from dataclasses import dataclass
from typing import TypedDict, Literal
from events.Event import BaseEvent

class CheerPayload(TypedDict):
    username: str
    bits: int
    message: str

@dataclass
class EventCheer(BaseEvent):
    name: Literal["twitch.cheer"] = "twitch.cheer"
    source: Literal["twitch"] = "twitch"
    payload: CheerPayload | None = None