import io
import logging
from random import randint
import traceback

from discord import File, Interaction, Message, Status, app_commands
from discord.ext import commands, tasks

from src.cogs.CocktowerCog import CocktowerCog
from src.cogs.IndependentCog import BIRTHDAY_ROLE, IndependentCog, check_birthday
from src.database import get_birthday_by_person, get_sounds, init, load_all_schemas

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
        
        self.tree.on_error = self.on_app_command_error
        
        await self.birthday_check()
    
    async def on_message(self, message: Message) -> None:
        await self.wait_until_ready()
        
        if self.user is None:
            return
        if self.user.mentioned_in(message):
            await message.channel.send(await get_random_msg())
        
        if self.user.id == self.correctSelfId and message.raw_mentions.count(self.fauxFriendId) > 0:
            if message.guild is not None and \
                (member := message.guild.get_member(self.fauxFriendId)) is not None:
                if member.status == Status.offline:
                    await message.channel.send("My fwiend is not online, don't bother")
            else:
                await message.channel.send("My fwiend is not here :<")
    
    async def on_app_command_error(self, interaction: Interaction, error: app_commands.AppCommandError) -> None:
        await interaction.response.defer()
        tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        logger.exception(f"Ignoring exception in command {"<none>" if interaction.command is None else interaction.command.name}:", exc_info=error)
        error_file = File(
            fp=io.BytesIO(tb.encode("utf-8")),
            filename="reason.txt"
        )
        
        await interaction.followup.send("Help, I'm crashing out!", file=error_file)
    
    @tasks.loop(hours=24)
    async def birthday_check(self):
        await self.wait_until_ready()
        
        if (main_server := self.get_guild(1093713117369868312)) and (birthday_role := main_server.get_role(BIRTHDAY_ROLE)):
            for member in main_server.members:
                user_id = member.id
                d = await get_birthday_by_person(user_id)
                if d is not None:
                    await check_birthday(d, member, birthday_role)