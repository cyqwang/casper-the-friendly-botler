# bot.py
import os
import json
# import random

# 1
import discord
from discord.ext import tasks, commands

intents = discord.Intents.default()
intents.members = True

setupfile = open("load/setup.json", "r")
setupdict = json.loads(setupfile.read())
setupfile.close()

TOKEN = setupdict['token']

#general bot meta
bot = commands.Bot(command_prefix='👻', intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_command_error(ctx, error):
	await ctx.send(error)

for filename in os.listdir("./cogs"):
	if filename.endswith(".py") and filename != "__init__.py":
		bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(TOKEN)