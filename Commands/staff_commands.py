import discord
import permission
from discord.ext import commands as client

class Staff:
    def __init__(self, bot):
        self.bot = bot

    @permission.is_staff()
    @client.command(pass_context = True)
    async def shutdown(self):
        print("ShutDown")
        await self.bot.logout()
        raise SystemExit

def setup(bot):
    bot.add_cog(Staff(bot))