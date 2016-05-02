import asyncio
import discord
import permission
from discord.ext import commands as client

class Staff:
    def __init__(self, bot):
        self.bot = bot
    #MANAGEMENT COMMANDS
    @permission.is_staff()
    @client.command(pass_context=True)
    async def ban(self, ctx, member:discord.Member, *args):
        try:
            await self.bot.ban(member)
            try:
                await self.bot.send_message(ctx.message.server.get_channel(const.alert_channel), '{0} Banned {1}. \nReason: {2}'.format(ctx.message.author.mention, member.mention, ''.join(args)))
            except:
                await self.bot.say('{0} Banned {1}'.format(ctx.message.author, member.name))
        except discord.errors.Forbidden:
            await self.bot.say('I dont have permission to ban {}'.format(member.name))
        except:
            return

    @permission.is_staff()
    @client.command(pass_context=True)
    async def kick(self,ctx, member:discord.Member, *args):
        try:
            await self.bot.kick(member)
            try:
                await self.bot.send_message(ctx.message.server.get_channel(const.alert_channel), '{0} kicked {1}. \nReason: {2}'.format(ctx.message.author.mention, member.mention, args))
            except:
                await self.bot.say('{0} kicked {1}'.format(ctx.message.author, member.name))
        except discord.errors.Forbidden:
            await self.bot.say('I dont have permission to kick {}'.format(member.name))
            return
        except:
            return

    #MESSAGE COMMANDS
    @permission.is_staff()
    @client.group(pass_context = True)
    async def clean(self, ctx, limit = 10):
        """Clean up to 500 messages in 2500ms"""
        if limit > 500:
            limit = 500
        if ctx.invoked_subcommand is None:
            limit = limit + 1
            asyncio.sleep(5)
            await self.delete(ctx.message.channel, limit, lambda predicate: True)

    async def delete(self, channel, limit, predicate):
        """This function is used to remove messages from a channel"""
        async for msg in self.bot.logs_from(channel, limit = limit):
            if predicate(msg):
                try:
                    await self.bot.delete_message(msg)
                except discord.Forbidden:
                    await self.bot.say('I dont have permission to delete messages!')
                    return
                except:
                    return

    #UPTIME COMMANDS
    @permission.is_staff()
    @client.command(pass_context = True)
    async def shutdown(self):
        """Shutdowns the bot //Please do not use unless you have to"""
        print("ShutDown")
        await self.bot.logout()
        raise SystemExit

def setup(bot):
    bot.add_cog(Staff(bot))