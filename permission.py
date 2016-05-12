import discord
import json
from discord.ext import commands as client
servers = json.loads(open('servers.json','r').read())

def check_if_staff(ctx):
    if check_if_admin(ctx) or check_if_mod(ctx) or check_if_owner(ctx):
        return True
    return False

def check_if_owner(ctx):
	if ctx.message.author.id == servers["Owner ID"]:
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
        for role in servers["Admin Roles"][i]:
            for user_role in ctx.message.author.roles:
                if str(user_role.id) == str(role):
                    return True
    return False

def is_staff():
	return client.check(check_if_staff)

def is_admin():
	return client.check(check_if_owner)

def is_admin():
	return client.check(check_if_admin)

def is_mod():
	return client.check(check_if_mod)
