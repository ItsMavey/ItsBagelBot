from functools import wraps


def broadcaster(func):
    """Only allow broadcaster."""
    @wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        if not ctx.get("is_broadcaster"):
            return "This command is for the broadcaster only."
        return await func(ctx, *args, **kwargs)
    return wrapper

def mod(func):
    """Only allow moderators or broadcaster."""
    @wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        if not (ctx.get("is_mod") or ctx.get("is_broadcaster")):
            return "This command is for moderators only."
        return await func(ctx, *args, **kwargs)
    return wrapper


def vip(func):
    """Only allow VIPs, mods, or broadcaster."""
    @wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        if not (ctx.get("is_vip") or ctx.get("is_mod") or ctx.get("is_broadcaster")):
            return "This command is for VIPs or higher."
        return await func(ctx, *args, **kwargs)
    return wrapper


def sub(func):
    """Only allow subscribers (and higher ranks)."""
    @wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        if not (ctx.get("is_sub") or ctx.get("is_vip") or ctx.get("is_mod") or ctx.get("is_broadcaster")):
            return "📺 This command is for subscribers or higher."
        return await func(ctx, *args, **kwargs)
    return wrapper