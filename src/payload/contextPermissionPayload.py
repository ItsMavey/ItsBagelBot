from typing import TypedDict


class Permission(TypedDict):
    is_broadcaster: bool
    is_mod: bool
    is_vip: bool
    is_subscriber: bool