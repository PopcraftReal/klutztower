from discord import Message
from discord.ext import commands
from discord import Status

from src.database import init, load_all_schemas, get_sounds
from src.cogs.IndependentCog import IndependentCog
from src.cogs.CocktowerCog import CocktowerCog
from random import randint

import logging

logger = logging.getLogger()

async def get_random_msg():
    msgs = await get_sounds()
    if len(msgs) - 1 == 0:
        return "Boo!"
    i = randint(0, len(msgs) - 1)
    return msgs[i]


class BotClient(commands.Bot):
    
    async def on_ready(self):
        await init()
        await load_all_schemas()
        logger.info("Add cogs...")
        await self.add_cog(CocktowerCog())
        await self.add_cog(IndependentCog())
        
        logger.info(f'Hello, I\'m ready! {self.user}')
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            logger.info(f"Error syncing commands: {e}")
        
        self.fauxFriendId: int = 1554846323184898169
        self.correctSelfId: int = 1517883899458617474
    
    async def on_message(self, message: Message) -> None:
        assert self.user is not None
        if self.user.mentioned_in(message):
            await message.channel.send(await get_random_msg())
        
        if self.user.id == self.correctSelfId and message.raw_mentions.count(self.fauxFriendId) > 0:
            if message.guild is not None and \
                (member := message.guild.get_member(self.fauxFriendId)) is not None:
                if member.status == Status.offline:
                    await message.channel.send("My fwiend is not online, don't bother")
            else:
                await message.channel.send("My fwiend is not here :<")