from database.models.TwitchCommands import TwitchCommands
from database.models.APITokens import APITokens
from database.models.BotUsers import BotUsers

# Register all models here
MODELS = [
    TwitchCommands,
    APITokens,
    BotUsers,
]