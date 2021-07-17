import discord
import json
import aiofiles
from discord.ext import commands
from discord.ext.commands import CommandNotFound

version = 'v0.4.1b'


def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=get_prefix,
    description='Amadeus is your helper day to day',
    owner_id=229698721498136576,
    case_insensitive=True,
    intents=intents
    )

bot.remove_command('help')


@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    bot.warnings[guild.id] = {}

    print(f"\n*{guild.name}* Has joined to the crew. His ID is {guild.id}\n")


@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    print(f"\n*{guild.name}* left.\n")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        embed = discord.Embed(title="ERROR", color=0x00d9ff)
        embed.set_author(name="Amadeus",
                         icon_url="https://media.discordapp.net/attachments/266409858666987520"
                                  "/830998897668521984/Amadeus-fondo-azul.jpg")
        embed.set_thumbnail(url="https://assets.prestashop2.com/sites/default/files/styles/blog_750x320"
                                "/public/wysiwyg/http_code_404_error.jpg?itok=jg7KKK_c")
        embed.add_field(name="Sorry mate", value="I can't find this command. Maybe you type it wrong", inline=False)
        embed.set_footer(text=f"Amadeus {version}")
        await ctx.send(embed=embed)
        return
    raise error


@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        pass

    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(bot.get_guild(
                        payload.guild_id).roles, id=x['role_id'])
                    await payload.member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name:
                role = discord.utils.get(bot.get_guild(
                    payload.guild_id).roles, id=x['role_id'])

                await bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
