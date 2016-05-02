import discord
from discord.ext import commands as client

class General:
    def __init__(self, bot):
        self.bot = bot

    @client.command()
    async def ping(self):
        #'''The bot replies with Pong!, Usage: {}ping'''.format(';')
        print('The bot replies with Pong!, Usage: {}ping'.format(';').__doc__)
        await self.bot.say('Pong!')


def setup(bot):
    bot.add_cog(General(bot))