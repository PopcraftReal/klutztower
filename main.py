import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

PREFIX = '-'

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"Hello, I'm ready! {bot.user.name}")

@bot.command()
async def wiki(ctx: commands.Context, *, characterName):
    if characterName == None:
        await ctx.send("Empty argument")
        return
    await ctx.send(f"Looking up {characterName}...")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)