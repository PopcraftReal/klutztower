import discord
from dotenv import load_dotenv
import os
from keep_alive import keep_alive

PREFIX = '-'
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if (TOKEN is None):
    raise Exception('No token found!')


class Client(discord.Client):

    async def on_ready(self):
        print(f'Hello, I\'m ready! {self.user}')


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = Client(intents=intents)
keep_alive()
client.run(TOKEN)
