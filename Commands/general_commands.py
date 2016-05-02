import discord
from discord.ext import commands as client

class General:
    def __init__(self, bot):
        self.bot = bot

    @client.command()
    async def ping(self):
        """The bot replies with Pong!, Usage: [prefix]ping"""
        await self.bot.say('Pong!')

    @client.command(pass_context = True)
    async def whois(self, ctx):
        if not "@here" in ctx.message.content or not "@everyone" in ctx.message.content:
            for mention in ctx.message.mentions:
        	    await self.bot.say('Username: {0.name}\nNickname: {0.nick}\nUserID: {0.id}\nUserDiscriminator: {0.discriminator}\nAvatar: {0.avatar}\nJoined the server: {0.joined_at}\nBot: {0.bot}'.format(mention))
        

def setup(bot):
    bot.add_cog(General(bot))