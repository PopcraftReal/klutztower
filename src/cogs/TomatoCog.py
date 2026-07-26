from discord import Embed, Interaction, app_commands
from discord.ext.commands import GroupCog

from specifics.tomato import retrieveMovie


class CocktowerCog(GroupCog, name="botc"):

    @app_commands.command(name="rate")
    async def get_rating(self, interaction: Interaction, movie_title: str):
        await interaction.response.defer()
        
        movie = retrieveMovie(movie_title.strip())
        if movie is None:
            return await interaction.followup.send(f"Movie '{movie_title}' not found on Rotten Tomatoes.")

        embed = Embed(title=movie.movie_title, 
                      url=movie.url,
                      description = movie.synopsis)
        movie.critics_consensus
        embed.set_thumbnail(url=movie.image)
        print(movie.image)
        embed.add_field(name="Duration", value=f"{movie.duration}")
        embed.add_field(name="Rating", value=f"{movie.rating}")
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name="🍅 Tomatometer", value=f"{movie.tomatometer}%")
        embed.add_field(name="🍿 Audience Score", value=f"{movie.audience_score}%")
        await interaction.followup.send(embed=embed)