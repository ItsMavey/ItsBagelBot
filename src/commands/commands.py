"""
This module serves as a command manager where it finds all command modules and registers them.

It will also parse the commands and invoke the functions with the decorated commands.
"""

from commands import COMMAND_REGISTRY

""" DO NOT REMOVE !!! """
from bot import components # Allow registration of commands via imports in the __init__.py file


class CommandManager:
    """Responsible for finding and executing commands."""
    def __init__(self):
        self.commands = COMMAND_REGISTRY  # all registered commands

    async def dispatch(self, ctx):
        """Parse and execute a command message."""

        if not ctx.command:
            return None

        # Find the command
        cmd = self.commands.get(ctx.command)
        if not cmd:
            return None

        func = cmd["func"]

        # Run the command safely
        try:
            result = await func(ctx)

            if result:
                await ctx.send(result)

        except TypeError as e:
            await ctx.send(f"Invalid usage: {e}")
        except Exception as e:
            await ctx.send(f"Error running command: {e}")