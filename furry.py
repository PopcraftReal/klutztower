import os
import logging
import sys

import discord
from dotenv import load_dotenv

from src.BotClient import BotClient


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO
)

PREFIX = '-'
intents = discord.Intents.all()

client = BotClient(command_prefix=PREFIX, intents=intents)

if __name__ == "__main__":
    load_dotenv()
    token: str | None = os.getenv('DISCORD_TOKEN')
    if token is None:
        token = ""
    client.run(token)