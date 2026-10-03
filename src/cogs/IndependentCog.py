from datetime import datetime
from enum import Enum
from random import randint
from zoneinfo import ZoneInfo
from math import inf

from discord import ChannelType, Colour, Embed, Interaction, User
from discord import app_commands
from discord.ext.commands import Cog
from discord.app_commands import Choice

from src.database import get_sounds

SYDNEY = ZoneInfo("Australia/Sydney")

LEVEL_1 = 3
LEVEL_2 = 6
LEVEL_3 = 9

class BatteryStatus(Enum):
    STATUS_HAPPY = "The user is happy with sufficient interaction"
    STATUS_DEPLETING = "The user is feeling rather down with interactions stop"
    STATUS_CRASHING = "The user is rather crashing because of self-isolation"
    STATUS_WORLDENDING = "The user is dead due to a lack of socialising"
    STATUS_CANT_ELABORATE = "The user hasn't sent a text in the last 500 texts. I think they're dead"

def cap(val: int | float, min: int | float = -inf, max: int | float = inf):
    if val < min:
        return min
    if val > max:
        return max
    return val

def getBatteryVisual(level: int) -> str:
    if level == -1:
        return ':negative_squared_cross_mark:'
    if level < 4:
        return ':red_square:'
    elif level < 7:
        return ':orange_square:'
    elif level < 10:
        return ':yellow_square:'
    return ':green_square:'

def getStatus(level: int) -> BatteryStatus:
    if level < 4:
        return BatteryStatus.STATUS_WORLDENDING
    elif level < 7:
        return BatteryStatus.STATUS_CRASHING
    elif level < 10:
        return BatteryStatus.STATUS_DEPLETING
    return BatteryStatus.STATUS_HAPPY

def createBatteryEmbed(user: User, status: BatteryStatus, level: int):
    embed = Embed(colour=Colour.pink())
    embed.set_author(name=f"Battery for {user.display_name}", icon_url=f"{user.display_avatar.url}")
    
    colour: str = getBatteryVisual(level)
    empty: str = ':black_large_square:'
    
    embed.title = "Battery"
    embed.description = f"""
    Status: {status.value}
    {colour * level}{empty * (12 - level)}
    """
    return embed

def get_random_msg():
    msgs = get_sounds()
    if len(msgs) - 1 == 0:
        return "Boo!"
    i = randint(0, len(msgs) - 1)
    return msgs[i]

SPR_CHOICES = [
    Choice(name="✂️", value=0),
    Choice(name="🪨", value=1),
    Choice(name="📰", value=2)
]

class IndependentCog(Cog):
    
    @app_commands.command(name="battery",
                          description="Get battery of owner")
    async def battery(self, interaction: Interaction, user: User):
        await interaction.response.defer()
        assert interaction.channel is not None
        
        if interaction.channel.type == ChannelType.text or \
            interaction.channel.type == ChannelType.private:
            send_time: datetime | None = None
            async for message in interaction.channel.history(limit=500):
                if message.author.id == user.id:
                    send_time = message.created_at
                    break
            
            status = BatteryStatus.STATUS_CANT_ELABORATE
            difference = -1
            
            if send_time is not None:
                now = datetime.now(SYDNEY)
                difference = cap(12 - ((now - send_time.astimezone(SYDNEY)).total_seconds() // 3600), 0, 12)
                status = getStatus(int(difference))
            
            embed = createBatteryEmbed(user, status, int(difference))
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("This makes no sense to me :3")
    
    @app_commands.command(name='fetch',
                          description='Fetch! Good doggie!')
    async def fetch(self, interaction: Interaction):
        await interaction.response.defer()
        await interaction.followup.send(get_random_msg())
    
    @app_commands.command(name='spr',
                          description='Play Scissors, Paper, Rock! with The Furry')
    @app_commands.choices(
        userPlay = SPR_CHOICES
    )
    async def spc(self, interaction: Interaction, userPlay: Choice[int]):
        furryPlay = randint(0, 2)
        
        msg = f"""
        I played {SPR_CHOICES[furryPlay]}, and you played {userPlay.name}\n
        """
        
        if userPlay.value == furryPlay:
            await interaction.response.send_message(msg + "Tie? 🙀")
        elif userPlay.value > furryPlay or (furryPlay == 2 and userPlay.value == 0):
            await interaction.response.send_message(msg + "AWAWAWAWA 😿😿😿")
        else:
            await interaction.response.send_message(msg + "yayy 😸!")