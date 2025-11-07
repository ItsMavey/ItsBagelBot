from dataclasses import dataclass
from typing import TypedDict, Literal
from events.Event import BaseEvent

class StreamOnlinePayload(TypedDict):
    title: str
    started_at: str
    category: str

@dataclass
class EventStreamOnline(BaseEvent):
    name: Literal["twitch.stream.online"] = "twitch.stream.online"
    source: Literal["twitch"] = "twitch"
    payload: StreamOnlinePayload = None



class StreamOfflinePayload(TypedDict):
    ended_at: str

@dataclass
class EventStreamOffline(BaseEvent):
    name: Literal["twitch.stream.offline"] = "twitch.stream.offline"
    source: Literal["twitch"] = "twitch"
    payload: StreamOfflinePayload | None = None