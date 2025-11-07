from datetime import datetime, UTC

from tasks import Task

from utils import SystemBUS
from events.tasks import EventAuthRefresh
from events.tasks.payloads import AuthRefreshPayload

class TokenRefreshTask(Task):
    def __init__(self):
        super().__init__(
            name="Refresh Token Task",
            description="Handles user authentication tasks.",
            interval= 30 * 60,  # every 30 minutes
        )

    async def execute(self):
        # Placeholder for actual authentication logic

        request = EventAuthRefresh(
            payload= AuthRefreshPayload(
                reason="Periodic token refresh",
                timestamp=datetime.now(UTC).isoformat(),
            )
        )
        self.amount_executions += 1

        await SystemBUS.publish(request)