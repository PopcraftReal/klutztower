import discord

from dotenv import load_dotenv
import os

from src.BotClient import BotClient

PREFIX = '-'
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = BotClient(command_prefix=PREFIX, intents=intents)

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(TOKEN)