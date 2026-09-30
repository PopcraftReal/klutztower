from discord import Message
from discord.abc import User
from discord.ext import commands
from discord import Status

from src.database import get_sounds
from src.cogs.CocktowerCog import CocktowerCog
from random import randint

def get_random_msg():
    msgs = get_sounds()
    i = randint(0, len(msgs) - 1)
    return msgs[i]


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
        
        self.fauxFriendId: int = 1554846323184898169
        self.fauxFriend: User | None = self.get_user(self.fauxFriendId)
        self.correctSelfId: int = 1517883899458617474
        self.correctSelf: User | None = self.get_user(self.correctSelfId)
    
    def isFriendMentioned(self, message: Message):
        return self.fauxFriend is not None and self.fauxFriend.mentioned_in(message)
    
    async def on_message(self, message: Message) -> None:
        assert self.user is not None
        if self.user.mentioned_in(message):
            await message.channel.send(get_random_msg())
        
        if self.user.id == self.correctSelfId:
            if self.isFriendMentioned(message):
                if message.guild is None or (member := message.guild.get_member(self.fauxFriendId)) is None:
                    await message.channel.send("My fwiend is not here :<")
                elif member.status == Status.offline:
                    await message.channel.send("My fwiend is not online, don't bother")