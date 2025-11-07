"""
This module handles application settings and configurations.

It provides all the secret keys, database configurations, and other
settings required for the application to run.

Doppler will be used to manage and inject these secrets into the environment.
"""

import os

from twitchAPI.type import AuthScope
from datetime import datetime, UTC

BOT_NAME = 'ItsBagelBot'
BOT_LOGIN = BOT_NAME.lower()

MAIN_BROADCASTER = os.getenv('MAIN_BROADCASTER', 'itsmavey').lower()

WAKE_UP_TIME = datetime.now(UTC)

SPECIAL_ID = os.getenv('SPECIAL_ID')

CONTACT = {
    'EMAIL': os.getenv('CONTACT_EMAIL', "contact@itsmavey.com"),
    'DISCORD': os.getenv('CONTACT_DISCORD', "https://discord.gg/SZ2remwSDv"),
}

SERVERS = [
    ("twitch", "irc.chat.twitch.tv")
]

SCOPES = {
    'bot': [
        AuthScope.CHAT_READ,
        AuthScope.CHAT_EDIT,
        AuthScope.USER_READ_CHAT,
        AuthScope.USER_WRITE_CHAT,
        AuthScope.USER_BOT,
        AuthScope.CHANNEL_BOT,
        AuthScope.MODERATOR_READ_FOLLOWERS,
    ],

    'broadcaster': [
        AuthScope.MODERATOR_READ_FOLLOWERS,
        AuthScope.USER_READ_CHAT,
        AuthScope.USER_READ_CHAT,
        AuthScope.USER_WRITE_CHAT,
    ]
}

DATABASE_ENGINE = os.getenv("DATABASE_ENGINE", "sqlite")

DATABASE = {
    'postgres': {
        "NAME": os.getenv("POSTGRES_DB"),
        "ENGINE": "postgres",
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": int(os.getenv("POSTGRES_PORT")),
    },

    'sqlite': {
        "NAME": "bagelbot.db",
        "ENGINE": "sqlite",
    }
}

SPOTIFY = {
    'CLIENT_ID': os.getenv('SPOTIFY_CLIENT_ID'),
    'CLIENT_SECRET': os.getenv('SPOTIFY_CLIENT_SECRET'),
    'REDIRECT_URI': os.getenv('SPOTIFY_REDIRECT_URI', 'http://127.0.0.1:8080')
}

TWITCH = {
    'CLIENT_ID': os.getenv('TWITCH_CLIENT_ID'),
    'CLIENT_SECRET': os.getenv('TWITCH_CLIENT_SECRET'),
    'REDIRECT_URI': os.getenv('TWITCH_REDIRECT', 'http://localhost:17563'),
}
