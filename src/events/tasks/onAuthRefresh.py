from dataclasses import dataclass
from typing import Literal
from events.Event import BaseEvent

from events.tasks.payloads import AuthRefreshPayload


@dataclass
class EventAuthRefresh(BaseEvent):
    name: Literal["tasks.auth.refresh"] = "tasks.auth.refresh"
    source: Literal["system"] = "system"
    payload: AuthRefreshPayload = None
