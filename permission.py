import discord
import json
from discord.ext import commands as client
servers = json.loads(open('servers.json','r').read())

def check_if_staff(ctx):
    print('Is Staff')
    print(check_if_admin(ctx))
    if check_if_admin(ctx):
        return True
    if check_if_mod(ctx):
        return True

    return False

def check_if_admin(ctx):
    for i, server in enumerate(servers["Server ID"]):
        for role in servers["Admin Roles"][i]:
            for user_role in ctx.message.author.roles:
                if str(user_role.id) == str(role):
                    return True
    return False

def check_if_mod(ctx):
    for i, server in enumerate(servers["Server ID"]):
        for roles in servers["Mod Roles"][i]:
            for role in roles:
                for user_role in ctx.message.author.roles:
                    if user_role == role:
                        return True
    return False

def is_staff():
	return client.check(check_if_staff)

def is_admin():
	return client.check(check_if_admin)

def is_mod():
	return client.check(check_if_mod)
