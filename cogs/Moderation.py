import discord
import json
import time
import asyncio
import sqlite3
from time import ctime
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import MissingPermissions
from events import version


class StaffCommands(commands.Cog):
    """
    Staff commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick', help='kick users (only admin)')
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed = discord.Embed(title="SERVER INFO", color=0x00d9ff)
        embed.set_author(name="Amadeus",
                         icon_url="https://media.discordapp.net/attachments/266409858666987520"
                                  "/830998897668521984/Amadeus-fondo-azul.jpg")
        embed.add_field(name=f"{member} has been kicked from this server", value=f"Reason: {reason}", inline=False)
        embed.set_footer(text=f"Amadeus")
        await ctx.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(":red_circle:  You don't have permission to use this command.")

    @commands.command(name='ban', help='Ban users (only admin)')
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embed = discord.Embed(title="SERVER INFO", color=0x00d9ff)
        embed.set_author(name="Amadeus",
                         icon_url="https://media.discordapp.net/attachments/266409858666987520"
                                  "/830998897668521984/Amadeus-fondo-azul.jpg")
        embed.add_field(name=f"{member} has been banned from this server", value=f"Reason: {reason}", inline=False)
        embed.set_footer(text=f"Amadeus")
        await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(":red_circle:  You don't have permission to use this command.")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member: int = 0):

        if member == 0 or not isinstance(int(member),
                                         int):
            embed = discord.Embed(description=":x: Input a **Valid User ID**", color=0xff0000)
            return await ctx.send(embed=embed)

        guild = ctx.message.guild
        members = get(guild.bans(),
                      id=member)
        await guild.unban(user=members, reason=None)
        embed = discord.Embed(description=":white_check_mark: **%s** has been **Unbanned!**" % member.name,
                              color=0x00ff00)
        return await ctx.send(embed=embed)

    @commands.command(name='clear', help='this command will clear msgs (only admin)')
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=5):
        embed = discord.Embed(title="Cleaning this channel", color=0x00d9ff)
        embed.set_author(name="Amadeus",
                         icon_url="https://media.discordapp.net/attachments/266409858666987520"
                                  "/830998897668521984/Amadeus-fondo-azul.jpg")
        embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com"
                                "/images?q=tbn:ANd9GcStiaMZy6RSR_yXAvlgkjnfU-tQc4v679ptRw&usqp=CAU")
        embed.add_field(name="Whait a second", value="This is bad... i need to clean all right now!", inline=False)
        embed.set_footer(text=f"Amadeus {version}")
        await ctx.send(embed=embed)
        time.sleep(3)
        await ctx.channel.purge(limit=amount)
        time.sleep(1.5)
        await ctx.send('Wow, im really fast', delete_after=5)

    @commands.command(name='prefix'.lower(), aliases=['changeprefix'], help='Change prefix on your guild')
    @commands.has_permissions(administrator=True)
    async def prefix_(self, ctx, prefix):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        embed = discord.Embed(title="SERVER INFO", description="Prefix system", color=0xfb00ff)
        embed.set_author(name="Amadeus",
                         icon_url="https://media.discordapp.net/attachments/266409858666987520/830998897668521984"
                                  "/Amadeus-fondo-azul.jpg")
        embed.add_field(name="The prefix has been changed", value=f"New prefix: {prefix} ", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='rr', help='Create new post to get roles (only admin)')
    @commands.has_permissions(administrator=True)
    async def rr(self, ctx, emoji, role: discord.Role, *, message):

        emb = discord.Embed(description=message)
        msg = await ctx.send(embed=emb)
        await msg.add_reaction(emoji)

        with open('reactrole.json') as json_file:
            data = json.load(json_file)

            new_react_role = {'role_name': role.name,
                              'role_id': role.id,
                              'emoji': emoji,
                              'message_id': msg.id}

            data.append(new_react_role)

        with open('reactrole.json', 'w') as f:
            json.dump(data, f, indent=4)
        '''-----------------------------------------------------------------------------------------'''
    @commands.command(name='voice', help='ex: !voice "name" "slots"')
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def voice_(self, ctx, name: str, slots: int):
        can = discord.utils.get(ctx.guild.roles, name="#everyone")
        cant = discord.utils.get(ctx.guild.roles, name="@everyone")
        guild = ctx.channel.guild
        qwerty = discord.utils.get(guild.categories, id=839719529370484766)
        destroy = 7200
        voice_channel = await guild.create_voice_channel(f"🎧 {name}", overwrites=None, category=qwerty)

        if name is None:
            return await ctx.send("You dont provide a name for your voicechannel")

        if slots is None:
            return await ctx.send("You dont provide de ammount of slots for your voicechannel")

        embed = discord.Embed(title="VoiceGenerator",
                              description="I will create the channel that you requested in the category: '「 ♟ 」「 和 」' ",
                              color=0xd80ec7)
        embed.set_author(name="Amadeus", icon_url="https://media.discordapp.net/attachments"
                                                  "/266409858666987520/830998897668521984/Amadeus-fondo-azul.jpg")
        embed.set_thumbnail(url="https://www.windowscentral.com/sites/wpcentral.com/files"
                                "/styles/large/public/field/image/2020/04/discord-voice-channel-1.jpg?itok=utpce9tA")
        embed.add_field(name=f"Successfully  [Channel Name : {name}] ",
                        value=f"[Slots requested : {slots}] - [State : Public]", inline=False)
        embed.add_field(name="The channel will be autodestroyed in :", value="[ 2 hours ]", inline=True)
        await ctx.send(embed=embed)
        await voice_channel.set_permissions(target=cant, connect=False, speak=False, view_channel=False)
        await voice_channel.set_permissions(target=can, connect=True, speak=True, view_channel=True)
        await voice_channel.edit(user_limit=slots, bitrate=384000)
        await asyncio.sleep(destroy)
        await voice_channel.delete(reason="Autodestroy by Amadeus")

    @voice_.error
    async def voice_handler(self, ctx, error):

        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send("You are on cooldown, you cant use this command for another 5 minutes.")

        if error.param.name == 'slots':
            await ctx.send("[ERROR] Command example: >voice 'name of the channel' 10 "
                           "(This need to be a integer this is de ammount of slots on the channel)")

    @commands.command(aliases=['tempmute'])
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member = None, time: int = None, *, reason=None):
        if not member:
            await ctx.send("You must mention a member to mute!")
        elif not time:
            await ctx.send("You must mention a time!")
        else:
            if not reason:
                reason = "No reason given"

        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role in member.roles:
            return await ctx.send(f"{member} is already muted")
        else:
            duration = time * 60
            guild = ctx.guild
            muted = discord.utils.get(guild.roles, name="Muted")
            if not muted:
                muted = await guild.create_role(name="Muted")
                for channel in guild.channels:
                    await channel.set_permissions(muted, speak=False, send_messages=False,
                                                  read_message_history=True, read_messages=False)
            await member.add_roles(muted, reason=reason)
            muted_embed = discord.Embed(title="Muted a user", description=f"{member.mention} "
                                                                          f"Was muted by {ctx.author.mention} for "
                                                                          f"{reason} to {time} minutes")
            await ctx.send(embed=muted_embed)
            print(duration)
            await asyncio.sleep(duration)
            await member.remove_roles(muted)
            unmute_embed = discord.Embed(title="Mute over!", description=f'{ctx.author.mention} '
                                                                         f'muted to {member.mention} for {reason} '
                                                                         f'is over after {time} minutes')
            await ctx.send(embed=unmute_embed)


def setup(bot):
    bot.add_cog(StaffCommands(bot))
