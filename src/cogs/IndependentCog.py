from datetime import datetime
from enum import Enum
from zoneinfo import ZoneInfo

from discord import ChannelType, Colour, Embed, Interaction, app_commands, User
from discord.ext.commands import Cog

SYDNEY = ZoneInfo("Australia/Sydney")

LEVEL_1 = 3
LEVEL_2 = 6
LEVEL_3 = 9

class BatteryStatus(Enum):
    STATUS_HAPPY = "The user is happy wiht sufficient interaction"
    STATUS_DEPLETING = "The user is feeling rather down with interactions stop"
    STATUS_CRASHING = "The user is rather crashing because of self-isolation"
    STATUS_WORLDENDING = "The user is dead"
    STATUS_CANT_ELABORATE = "The user hasn't sent a text in the last 500 texts. I think they're dead"

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
    embed.set_author(name=f"Battery for {user.name}", icon_url=f"{user.display_avatar.url}")
    
    colour: str = getBatteryVisual(level)
    empty: str = ':black_large_square:'
    
    embed.title = "Battery"
    embed.description = f"""
    Status: {status.value}
    {colour * level}{empty * (12 - level)}
    """
    return embed

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
                difference = 12 - ((now - send_time.astimezone(SYDNEY)).seconds // 3600)
                status = getStatus(difference)
            
            embed = createBatteryEmbed(user, status, difference)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("This makes no sense to me :3")