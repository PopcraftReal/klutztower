import discord
from dotenv import load_dotenv
import os

PREFIX = '-'
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class Client(discord.Client):
    async def on_ready(self):
        print(f'Hello, I\'m ready! {self.user}')
    
    async def on_message(self, msg: discord.Message):
        print(f"Message from {msg.author}: {msg.content}")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = Client(intents=intents)
client.run(TOKEN)