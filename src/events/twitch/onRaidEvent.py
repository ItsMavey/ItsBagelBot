from dataclasses import dataclass
from typing import TypedDict, Literal
from events.Event import BaseEvent

class RaidInPayload(TypedDict):
    from_broadcaster: str
    viewers: int

@dataclass
class EventRaidIn(BaseEvent):
    name: Literal["twitch.raid.in"] = "twitch.raid.in"
    source: Literal["twitch"] = "twitch"
    payload: RaidInPayload | None = None


class RaidOutPayload(TypedDict):
    to_broadcaster: str
    viewers: int

@dataclass
class EventRaidOut(BaseEvent):
    name: Literal["twitch.raid.out"] = "twitch.raid.out"
    source: Literal["twitch"] = "twitch"
    payload: RaidOutPayload | None = None

