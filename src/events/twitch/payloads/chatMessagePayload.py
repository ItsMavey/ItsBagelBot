from typing import TypedDict

from payload import Permission

class ChatMessagePayload(TypedDict):
    username: str
    user_id: str
    message: str
    is_mod: bool
    is_vip: bool
    is_subscriber: bool

class ChatCommandPayload(TypedDict):
    username: str
    user_id: str
    command: str

    permission: Permission

