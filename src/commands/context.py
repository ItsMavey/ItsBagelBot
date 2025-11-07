from API import HELIX
from events.tasks import EventChatRequest
from events.tasks.payloads import ChatRequestPayload
from utils import EventBUS


class Context:
    """Lightweight context object passed to commands."""
    def __init__(self, user, id, message, badges=None, send_func=None):
        self.user = user
        self.id = id
        self.raw_message = message

        if message.startswith("!"):

            content = message[1:].strip()

            if not content: # if message is just "!"
                self.command = None
                self.message = ""
            else:
                parts = content.split(maxsplit=1)
                self.command = parts[0].lower()
                self.message = parts[1] if len(parts) > 1 else ""

        else:
            self.command = None
            self.message = message.strip()

        self.badges = badges or []
        self.send_func = send_func

        # Permission flags from Twitch badges
        self.is_broadcaster = "broadcaster" in self.badges
        self.is_mod = "moderator" in self.badges or self.is_broadcaster
        self.is_vip = "vip" in self.badges
        self.is_sub = "subscriber" in self.badges

    async def send(self, text: str):
        """Send a message back to chat using either the custom sender or Helix."""
        if self.send_func:
            # Use the provided send function (e.g., test or IRC-level sender)
            try:
                if callable(self.send_func):
                    # Handle both sync and async send functions
                    result = self.send_func(text)
                    if hasattr(result, "__await__"):
                        await result
                else:
                    print(f"[WARN] send_func is not callable: {self.send_func}")
            except Exception as e:
                print(f"[ERROR] send_func failed: {e}")

            return

        request_event = EventChatRequest(
            payload=ChatRequestPayload(
                message="🥯🥯🥯🥯🥯🥯🥯🥯🥯🥯🥯🥯🥯\n🥯🥯🥯🥯🥯🥯🥯🥯🥯🥯🥯🥯🥯\n🥯🥯🥯🥯🥯🥯🥯🥯🥯🥯🥯🥯🥯",
            )
        )

        await EventBUS.publish(request_event)



    def __repr__(self):
        return f"<Context user={self.user} badges={self.badges}>"