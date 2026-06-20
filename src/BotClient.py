from discord.ext import commands

class BotClient(commands.Bot):
    async def on_ready(self):
        print(f'Hello, I\'m ready! {self.user}')

        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"Error syncing commands: {e}")