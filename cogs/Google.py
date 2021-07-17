import discord
from discord.ext import commands
from googlesearch import search


class Search(commands.Cog):
    """
    Online search
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='google', aliases=['goo'])
    async def googlesearch_(self, ctx, s: str):
        googleimg = 'https://www.muycomputer.com/wp-content/uploads/2020/12/Servicios_de_Google.png'
        for primera in search(s, num_results=0, lang="es"):
            for segunda in search(s, num_results=0, lang="es"):
                for tercera in search(s, num_results=0, lang="es"):
                    embed = discord.Embed(title="Google Search", url="https://www.google.com",
                                          description="These are the first 3 links I found for you", color=0x00f010)
                    embed.set_thumbnail(url=googleimg)
                    embed.add_field(name="LINK", value=primera, inline=False)
                    embed.add_field(name="LINK", value=segunda, inline=True)
                    embed.add_field(name="LINK", value=tercera, inline=True)
                    embed.set_footer(text="Amadeus - Google search by karma.1N")
                    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Search(bot))
