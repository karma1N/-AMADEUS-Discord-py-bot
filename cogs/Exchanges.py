import discord
import requests
import json
import asyncio
from discord.ext import commands
from events import version


class Exchanges(commands.Cog):
    """
    Check the current price of your favorite crypto on Binance/Gate.io
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def binance(self, ctx, symbol: str):
        """
        Example: .binance BTCUSDT
        """
        response = requests.get("https://api.binance.com/api/v1/ticker/24hr?symbol=" + symbol.upper())
        ticket = json.loads(response.text)
        embed = discord.Embed(title=f"Current Price of {symbol} on ", url="https://www.binance.com",
                              color=0x1bed07)
        embed.set_author(name="Amadeus",
                         icon_url="https://media.discordapp.net/attachments/266409858666987520"
                                  "/830998897668521984/Amadeus-fondo-azul.jpg")
        embed.set_thumbnail(
            url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHKWN2PY4_YYGGkSafw2l8c6wQwu_gf2eRCw&usqp=CAU")
        embed.add_field(name="CURRENT:", value=f"${ticket['lastPrice']}", inline=True)
        embed.add_field(name="24H % CHANGE:", value=f"{ticket['priceChangePercent']}%", inline=True)
        embed.add_field(name="OPEN:", value=f"${ticket['openPrice']}", inline=False)
        embed.add_field(name="HIGH:", value=f"${ticket['highPrice']}", inline=True)
        embed.add_field(name="LOW:", value=f"${ticket['lowPrice']}", inline=True)
        embed.set_footer(text=f"Amadeus {version}")
        await ctx.send(embed=embed)

    @commands.command()
    async def alert(self, ctx, symbol: str, target):
        """
        Working on this
        """
        with open('binancealerts.json') as json_file:
            data = json.load(json_file)

            newalert = {"symbol": symbol,
                        "price": target}

            data.append(newalert)

        with open('binancealerts.json', 'w') as f:
            json.dump(data, f, indent=2)

        embed = discord.Embed(title="Alert", color=0x1ae208)
        embed.set_author(name="Amadeus", icon_url="https://media.discordapp.net/attachments/266409858666987520/"
                                                  "830998897668521984/Amadeus-fondo-azul.jpg")
        embed.set_thumbnail(
            url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHKWN2PY4_YYGGkSafw2l8c6wQwu_gf2eRCw&usqp=CAU")
        embed.add_field(name=f"Se agrego exitosamente una alerta en: {symbol}",
                        value=f'Cuando su precio sea igual o mayor a {target} te avisare!', inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def alertlist(self, ctx):
        with open('binancealerts.json') as json_file:
            json_object = json.load(json_file)
            json_formatted_str = json.dumps(json_object, indent=2)

            await ctx.send(json_formatted_str)

    @commands.command()
    async def gate(self, ctx, symbol: str):
        """
        Example: .gate BTC_USDT
        """
        response = requests.get("https://data.gateapi.io/api2/1/ticker/" + symbol.upper())
        ticket = json.loads(response.text)
        embed = discord.Embed(title=f"Current Price of {symbol} on ", url="https://www.gate.io",
                              color=0x1bed07)
        embed.set_author(name="Amadeus",
                         icon_url="https://media.discordapp.net/attachments/266409858666987520"
                                  "/830998897668521984/Amadeus-fondo-azul.jpg")
        embed.set_thumbnail(
            url='https://coinlist.me/wp-content/uploads/2020/09/gateio-logo.png')
        embed.add_field(name="CURRENT:", value=f"${ticket['last']}", inline=True)
        embed.add_field(name="24H % CHANGE:", value=f"{ticket['percentChange']}%", inline=True)
        embed.add_field(name="HIGH24h:", value=f"${ticket['high24hr']}", inline=True)
        embed.add_field(name="LOW24h:", value=f"${ticket['low24hr']}", inline=True)
        embed.set_footer(text=f"Amadeus {version}")
        await ctx.send(embed=embed)


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.pricealerts())

    async def pricealerts(self):
        await self.wait_until_ready()
        print('Estoy loopeando como un rey.')
        '''json1 = {
            "a": "b",
            "c": "d"
        }
        json2 = {
            "c": "d",
            "a": "b"
        }
        json1 = json.dumps(json1, sort_keys=True)
        json2 = json.dumps(json2, sort_keys=True)
        print(json1 == json2)'''
        await asyncio.sleep(60)  # task runs every 60 seconds


client = MyClient()


def setup(bot):
    bot.add_cog(Exchanges(bot))
