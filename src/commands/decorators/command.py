from functools import wraps

from commands import COMMAND_REGISTRY

def command(name=None, aliases=None, description=None):
    """
    Decorator to mark a function as a bot command.

    Args:
        name (str): Optional custom name for the command. Defaults to the function name.
        aliases (list[str]): Alternative trigger names for the command.
        description (str): Short description for help menus.
    """
    def decorator(func):
        cmd_name = name or func.__name__
        aliases_list = aliases or []

        # Keep original metadata for help/rebinding
        func.__command_meta__ = {
            "name": cmd_name,
            "aliases": aliases_list,
            "description": description or "",
        }

        @wraps(func)
        async def wrapper(*args, **kwargs):
            # The real callable used at runtime
            return await func(*args, **kwargs)

        # ✅ Register the WRAPPER so that any outer decorators (mod, vip, etc.)
        # applied later are still respected when invoked
        COMMAND_REGISTRY[cmd_name] = {
            "func": wrapper,
            "aliases": aliases_list,
            "description": description or "",
        }

        # ✅ Rebind aliases to the same registry entry (same dict)
        for alias in aliases_list:
            COMMAND_REGISTRY[alias] = COMMAND_REGISTRY[cmd_name]

        return wrapper  # important for decorator chaining

    return decorator