from dataclasses import dataclass
from typing import TypedDict, Literal
from events.Event import BaseEvent

class SubscriptionPayload(TypedDict):
    username: str
    tier: str
    cumulative_months: int
    is_gift: bool

@dataclass
class EventSubscription(BaseEvent):
    name: Literal["twitch.subscription"] = "twitch.subscription"
    source: Literal["twitch"] = "twitch"
    payload: SubscriptionPayload | None = None


class GiftedSubPayload(TypedDict):
    gifter_name: str
    recipient_name: str
    tier: str
    total_gifted: int

@dataclass
class EventGiftedSub(BaseEvent):
    name: Literal["twitch.subscription.gifted"] = "twitch.subscription.gifted"
    source: Literal["twitch"] = "twitch"
    payload: GiftedSubPayload | None = None
