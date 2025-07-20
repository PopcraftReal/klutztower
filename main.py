import discord
from dotenv import load_dotenv
import os
from keep_alive import keep_alive

from discord.ext import commands
from discord import app_commands

import urllib.request as req

try: 
    from BeautifulSoup import BeautifulSoup # type: ignore
except ImportError:
    from bs4 import BeautifulSoup

import botc

PREFIX = '-'
CLOCKTOWER_URL = "https://wiki.bloodontheclocktower.com/"

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if (TOKEN is None):
    raise Exception('No token found!')


class Client(commands.Bot):

    async def on_ready(self):
        print(f'Hello, I\'m ready! {self.user}')

        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"Error syncing commands: {e}")


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = Client(command_prefix=PREFIX, intents=intents)


@client.tree.command(name="wiki",
                     description="Retrieve wikipedia page of a character")
async def wiki(interaction: discord.Interaction, character: str):
    imageLink = f"{CLOCKTOWER_URL}File:Icon_{botc.clean(character)}.png"
    await interaction.response.send_message(imageLink)


keep_alive()
client.run(TOKEN)
