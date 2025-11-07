from dataclasses import dataclass
from typing import TypedDict, Literal
from events.Event import BaseEvent

class FollowPayload(TypedDict):
    username: str

@dataclass
class EventFollow(BaseEvent):
    name: Literal["twitch.follow"] = "twitch.follow"
    source: Literal["twitch"] = "twitch"
    payload: FollowPayload | None = None
