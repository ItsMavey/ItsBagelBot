"""
Defines a base event structure for an event-driven architecture.
"""

from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Dict, Any
import uuid

@dataclass
class BaseEvent:
    """Common structure for all events."""
    name: str
    source: str
    payload: Dict[str, Any]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self):
        if not self.name:
            raise ValueError("Event must have a name")
        if not self.source:
            raise ValueError("Event must have a source")

    def __str__(self):
        return f"<{self.name} from {self.source} at {self.timestamp.isoformat()}>"