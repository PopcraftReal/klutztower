from discord.ext import commands

from src.cogs.CocktowerCog import CocktowerCog

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