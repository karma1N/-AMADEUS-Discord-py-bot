import requests
from discord.ext import commands


URL = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
dolar = requests.get(URL).json()


class DolarHoy(commands.Cog):
    """
    Check pair U$D/AR$
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dolarhoy(self, ctx):
        await ctx.send('💵  | compra | venta ')
        await ctx.send('----|----------|-------')

        for index, emoji in enumerate(('🟢', '🔵')):
            compra = dolar[index]['casa']['compra'][:-1]
            venta = dolar[index]['casa']['venta'][:-1]

            await ctx.send(f" {emoji} |  {compra}  | {venta}")


def setup(bot):
    bot.add_cog(DolarHoy(bot))
