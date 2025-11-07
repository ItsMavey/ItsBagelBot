import asyncio

from database import setup

setup.initialize_database()
setup.auto_migrate()

from network import eventSub
from API import TWITCHAPI
from bot.twitch import TwitchBot

from tasks import TokenRefreshTask


async def main():
    TwitchBot()

    token_refresh_task = TokenRefreshTask()
    # Start token refresher as a background task
    asyncio.create_task(token_refresh_task.start())

    # Start EventSub
    await eventSub.main()


if __name__ == "__main__":
    asyncio.run(main())