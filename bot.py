"""
Name: TGC_Admin
Author: Estrobeda
Git_Repository: https://github.com/Estrobeda/tgc_admin
Description: TGC_Admin is an administrative bot for The Geek Corner
Licence: GPL-3.0
"""

import asyncio
import discord
import datetime
import json
import logging
import os, sys
from discord.ext import commands

try:
    setup = json.loads(open('setup.json','r').read())
except Exception as e:
    print('If you dont use the json setups you can ignore this Error')
    print(e, '\n\n')
finally:
    info = json.loads(open('info.json','r').read())
    extensions = json.loads(open('extensions.json','r').read())
    servers = json.loads(open('servers.json','r').read())

try:
    bot = commands.Bot([str(os.environ["TGC_Mention"]), str(os.environ["TGC_Prefix"])], description = info["Description"], pm_help = bool(os.environ["TGC_PM_Help"]))
    prefix = str(os.environ["TGC_Prefix"])
except Exception as e:
    print(e);
    bot = commands.Bot([setup["Mention"], setup["Prefix"]], description = info["Description"], pm_help = True)
    prefix = setup["Prefix"]
bot.commands_executed = 0
bot.unique_users = 0

#Data logging
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='TGCBot.log', encoding='utf-8', mode='w')
log.addHandler(handler)

@bot.event
async def on_ready():
    bot.change_status(game = discord.Game(game = ':help'))
    print('\Bot Log/')
    print('    \Bot Login/')
    print('    Logged in as : {0.user.name} {0.user.id}'.format(bot))
    print('    \Loading Commands')
    try:
        for extension in extensions["Commands"]:
            bot.load_cog(extensions)
    except:
        print('    No commands to be loaded')

@bot.event
async def on_member_join(member):
    i = 0
    for i, server in enumerate(servers["Server ID"]):
        if member.server.id == server:
            print(servers["Welcome Channel"][i])
            for channel in servers["Welcome Channel"][i]:
                print('{0.name} Joined the server, Sending welcome message to {1}'.format(member, channel))
                await bot.send_message(member.server.get_channel(channel), info["Welcome Message"] + member +  member.server.name)

@bot.event
async def on_command(cmd, ctx):
    command = ctx.message
    try:
        if not ctx.message.author in bot.unique_users:
            bot.unique_users += 1
        bot.process_commands(cmd)
        bot.commands_executed += 1
        log.info('{0}: {1.author.name} in {2}: {1.content}'.format(message.timestamp.replace(microsecond = 0 ), message, destination))
        print('{0}: {1.author.name} in {2}: {1.content}'.format(message.timestamp.replace(microsecond = 0 ), message, destination))
    except:
        log.info('	[!COMMAND_ERROR!] {0}: {1.author} {1.server} >>> Command: {1.content} Error: {2}'.format(ctx.message.timestamp.replace(microsecond = 0 ), ctx.message, error))
        print('	[!COMMAND_ERROR!] {0}: {1.author} in {1.server} >>> Command: {1.content} Error: {2}'.format(ctx.message.timestamp.replace(microsecond = 0 ), ctx.message, error))

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.DisabledCommand):
        await bot.say('srry but this command is disabled and cannot be used')
    else:
        log.info('	[!COMMAND_ERROR!] {0}: {1.author} {1.server} >>> Command: {1.content} Error: {2}'.format(ctx.message.timestamp.replace(microsecond = 0 ), ctx.message, error))
		
try:
    bot.run(str(os.environ["TGC_Token"]))
except Exception as e:
    print(e)
    bot.run(setup["Token"])

if discord.errors.ConnectionClosed:
	asyncio.sleep(5000)
	python = sys.executable
	os.execl(python, python, * sys.argv)