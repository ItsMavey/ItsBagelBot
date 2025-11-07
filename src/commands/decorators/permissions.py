from functools import wraps

def broadcaster(func):
    """Only allow broadcaster."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Handle both methods (self, ctx) and free functions (ctx)
        ctx = args[1] if len(args) >= 2 else args[0]

        if not getattr(ctx, "is_broadcaster", False):
            return None
        return await func(*args, **kwargs)
    return wrapper


def mod(func):
    """Only allow moderators or broadcaster."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        ctx = args[1] if len(args) >= 2 else args[0]

        if not (getattr(ctx, "is_mod", False) or getattr(ctx, "is_broadcaster", False)):
            return None
        return await func(*args, **kwargs)
    return wrapper


def vip(func):
    """Only allow VIPs, mods, or broadcaster."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        ctx = args[1] if len(args) >= 2 else args[0]

        if not (
                getattr(ctx, "is_vip", False)
                or getattr(ctx, "is_mod", False)
                or getattr(ctx, "is_broadcaster", False)
        ):
            return None
        return await func(*args, **kwargs)
    return wrapper


def sub(func):
    """Only allow subscribers (and higher ranks)."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        ctx = args[1] if len(args) >= 2 else args[0]

        if not (
                getattr(ctx, "is_subscriber", False)
                or getattr(ctx, "is_vip", False)
                or getattr(ctx, "is_mod", False)
                or getattr(ctx, "is_broadcaster", False)
        ):
            return None
        return await func(*args, **kwargs)
    return wrapper