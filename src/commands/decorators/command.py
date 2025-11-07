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
        cmd_name = name or func.__name__  # use provided name or function name
        aliases_list = aliases or []

        # Attach metadata for later rebinding if needed
        func.__command_meta__ = {
            "name": cmd_name,
            "aliases": aliases_list,
            "description": description or "",
        }

        # Store the function and metadata in the registry
        COMMAND_REGISTRY[cmd_name] = {
            "func": func,
            "aliases": aliases_list,
            "description": description or ""
        }

        # Also register each alias to point to the same command
        for alias in aliases_list:
            COMMAND_REGISTRY[alias] = COMMAND_REGISTRY[cmd_name]

        @wraps(func)
        async def wrapper(*args, **kwargs):
            # just wrap it so it can be called normally later
            return await func(*args, **kwargs)

        return wrapper

    return decorator