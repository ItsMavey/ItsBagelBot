from commands import context

COMMAND_REGISTRY = {}

from commands.commands import CommandManager
from commands.context import Context

COMMAND_MANAGER = CommandManager()