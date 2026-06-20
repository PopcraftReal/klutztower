from discord import Interaction, app_commands, Embed
from discord.ext.commands import GroupCog
from src.specifics import botc

DELAY = 60 * 15
CLOCKTOWER_URL = "https://wiki.bloodontheclocktower.com/"

class CocktowerCog(GroupCog, name="botc"):
    
    @app_commands.command(name="jinx", 
                          description="Retrieve Jinxes of a character")
    async def jinx(self, interaction: Interaction, character: str):
        title = botc.title(character)
        wikiURL = f"{CLOCKTOWER_URL}{botc.URLify(title)}"
        imageLink = f"{CLOCKTOWER_URL}File:Icon_{botc.clean(character)}.png"
        iconURL = botc.retrieveImageURL(imageLink)
        if iconURL == "":
            await interaction.response.send_message("Character not found")
            return

        jinxes = botc.getJinxes(wikiURL)
        embed = Embed(title=title, url=wikiURL)
        embed.set_thumbnail(url=iconURL)
        for jinx in jinxes:
            embed.add_field(name=jinx[0], value=jinx[1], inline=False)
        if len(jinxes) == 0:
            embed.description = "No jinx found"

        await interaction.response.send_message(embed=embed, delete_after=DELAY)
    
    @app_commands.command(name="wiki",
                          description="Retrieve Summary of a character")
    async def wiki(interaction: Interaction, character: str):
        title = botc.title(character)
        wikiURL = f"{CLOCKTOWER_URL}{botc.URLify(title)}"
        imageLink = f"{CLOCKTOWER_URL}File:Icon_{botc.clean(character)}.png"
        iconURL = botc.retrieveImageURL(imageLink)
        if iconURL == "":
            await interaction.response.send_message("Character not found")
            return
        descriptions = botc.getDescription(wikiURL)
        if descriptions[0] == "":
            await interaction.response.send_message("Something went wrong")
            return
        embed = Embed(title=title,
                            url=wikiURL,
                            description=descriptions[0])
        embed.set_thumbnail(url=iconURL)
        embed.add_field(name="Summary",
                        value=descriptions[1])

        await interaction.response.send_message(embed=embed, delete_after=DELAY)