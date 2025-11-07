import asyncio

from irctokens import build, Line
from ircrobots import Bot as BaseBot
from ircrobots import Server as BaseServer
from ircrobots import ConnectionParams

from API import TWITCHAPI
from utils.settings import BOT_NAME, SERVERS

@DeprecationWarning
class Server(BaseServer):

    async def line_read(self, line: Line):
        """ Called when a line is received from the server."""

        print(f"{self.name} < {line.format()}")
        if line.command == "001":
            await self.send(build("JOIN", [f"#{TWITCHAPI.channel}"]))

        if line.command == "PRIVMSG":
            channel = line.params[0]
            message = line.params[1]
            username = line.hostmask.nickname
            await self.on_message(username, channel, message)

    async def line_send(self, line: Line):
        print(f"{self.name} > {line.format()}")

    async def on_message(self, username: str, channel: str, message: str):
        print(f"[{channel}] <{username}> {message}")

        if message.strip().lower() == "!ping":
            await self.send_message(channel, f"@{username} Pong! 🏓")

    async def send_message(self, channel: str, message: str):
        await self.send(build("PRIVMSG", [channel, message]))
        print(f"[{channel}] {BOT_NAME} {message}")


class Bot(BaseBot):
    def create_server(self, name: str):
        return Server(self, name)

async def main():
    bot = Bot()
    for name, host in SERVERS:
        params = ConnectionParams(
            nickname=BOT_NAME,
            host=host,
            port=6697,
            password=f"oauth:{TWITCHAPI.BOT['oauth_token']}",
            username=BOT_NAME,
        )
        await bot.add_server(name, params)

    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())