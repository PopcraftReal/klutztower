import discord
from dotenv import load_dotenv
import os

from discord.ext import commands
from discord import app_commands

import urllib.request as req

import botc
from keep_alive import keep_alive

PREFIX = '-'
DELAY = 60 * 15
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
                     description="Retrieve Summary of a character")
async def wiki(interaction: discord.Interaction, character: str):
    title = botc.title(character)
    wikiURL = f"{CLOCKTOWER_URL}{botc.URLify(title)}"
    imageLink = f"{CLOCKTOWER_URL}File:Icon_{botc.clean(character)}.png"
    iconURL = botc.retrieveImageURL(imageLink)
    if iconURL == "":
        await interaction.response.send_message("Character not found")
        return
    descriptions = botc.getDescription(wikiURL)
    if descriptions[0] == "":
        await interaction.response.send_message("Something went wrong")
        return
    embed = discord.Embed(title=title,
                          url=wikiURL,
                          description=descriptions[0])
    embed.set_thumbnail(url=iconURL)
    embed.add_field(name="Summary",
                    value=descriptions[1] + "\n" + descriptions[2])

    await interaction.response.send_message(embed=embed, delete_after=DELAY)


@client.tree.command(name="jinx", description="Retrieve Jinxes of a character")
async def jinx(interaction: discord.Interaction, character: str):
    title = botc.title(character)
    wikiURL = f"{CLOCKTOWER_URL}{botc.URLify(title)}"
    imageLink = f"{CLOCKTOWER_URL}File:Icon_{botc.clean(character)}.png"
    iconURL = botc.retrieveImageURL(imageLink)
    if iconURL == "":
        await interaction.response.send_message("Character not found")
        return

    jinxes = botc.getJinxes(wikiURL)
    embed = discord.Embed(title=title, url=wikiURL)
    embed.set_thumbnail(url=iconURL)
    for jinx in jinxes:
        embed.add_field(name=jinx[0], value=jinx[1], inline=False)
    if len(jinxes) == 0:
        embed.description = "No jinx found"

    await interaction.response.send_message(embed=embed, delete_after=DELAY)

keep_alive()
client.run(TOKEN)