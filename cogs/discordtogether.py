import discord
from discord.ext import commands
from discordTogether import DiscordTogether


class YoutubeTogetherCog(commands.Cog):
    """
    Start app;s to play with the people of the voicechannel

    """
    def __init__(self, bot):
        self.bot = bot
        self.togetherControl = DiscordTogether(bot)

    @commands.command()
    @commands.cooldown(1, 150, commands.BucketType.user)
    async def start(self, ctx, activity: str):
        link = await self.togetherControl.create_link(ctx.author.voice.channel.id, activity)
        await ctx.send(f"Click the blue link!\n{link}")

    @start.error
    async def start_handler(self, ctx, error):
        embed = discord.Embed(title="[Discord Together]",
                              description="[+] Error: The name of the activity is not found. ", color=0xff0400)
        embed.set_author(name="Amadeus",
                         icon_url="https://media.discordapp.net/attachments/266409858666987520"
                                  "/830998897668521984/Amadeus-fondo-azul.jpg")
        embed.add_field(name="example:", value=".start youtube", inline=False)
        embed.add_field(name="[+] The list of the activitys:", value="[Youtube - Poker - Chess - Betrayal - Fishing]",
                        inline=True)
        if error.param.name == 'activity':
            await ctx.send(embed=embed)

        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send("You are on cooldown, you cant use this command for another 5 minutes.")


def setup(bot):
    bot.add_cog(YoutubeTogetherCog(bot))
