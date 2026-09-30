import os

import discord
from dotenv import load_dotenv

from database import init, run_schema
from src.BotClient import BotClient

PREFIX = '-'
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = BotClient(command_prefix=PREFIX, intents=intents)

if __name__ == "__main__":
    load_dotenv()
    token: str | None = os.getenv('DISCORD_TOKEN')
    if token is None:
        token = ""
    init()
    run_schema("./sql_schemas/01-setup.sql")
    client.run(token)