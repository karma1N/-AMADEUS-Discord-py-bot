import os
from status import status
from discord.ext import tasks
from events import *


@bot.event
async def on_ready():
    change_status.start()

    guild_count = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1
    print("\nSuccessfully connected to the network\n")


@tasks.loop(seconds=3)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


for filename in os.listdir('C:/Users/adrie/PycharmProjects/Amadeus/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


if __name__ == '__main__':
    bot.run('NDU5NTg3NTIzMjU4MzUxNjE3.WyyGPA.ozLWMuBRODzBkFk08nJx8gYXIXQ')
