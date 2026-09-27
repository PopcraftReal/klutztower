from discord import Message
from discord.ext import commands

from src.cogs.CocktowerCog import CocktowerCog
from random import randint

MSGS = ["Meow!", "Nya!", "Woof!", "Awawawa!", "Awoo!"]

def get_random_msg():
    i = randint(0, len(MSGS) - 1)
    return MSGS[i]

class BotClient(commands.Bot):
    async def on_ready(self):
        print("Add cogs...")
        await self.add_cog(CocktowerCog())
        
        print(f'Hello, I\'m ready! {self.user}')
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"Error syncing commands: {e}")
    
    async def on_message(self, message: Message) -> None:
        assert self.user is not None
        if self.user.mentioned_in(message):
            await message.channel.send(get_random_msg())