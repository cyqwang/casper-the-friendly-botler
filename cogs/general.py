# 1
import discord
from discord.ext import tasks, commands

import json
setupfile = open("load/setup.json", "r")
setup = json.loads(setupfile.read())
setupfile.close()

class General(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='help')
	async def help(self, ctx):
		await ctx.send("Check out my help documentation at https://tinyurl.com/CasperReference")

	@commands.command(name='get-txt-channel-id', help='get #text-channel id')
	async def get_txt_id(self, ctx, channel: discord.TextChannel):
		await ctx.send(channel.id)

	@commands.command(name='get-vox-channel-id', help='get #voice-channel id')
	async def get_vox_id(self, ctx, channel: discord.VoiceChannel):
		await ctx.send(channel.id)

	@commands.command(name='get-member-id', help='get member id')
	async def get_cat_id(self, ctx, member: discord.User):
		await ctx.send(member.id)

	@commands.command(name="load")
	@commands.is_owner()
	async def load(self, ctx, cog:str):
		try:
			self.bot.load_extension(cog)
		except Exception as e:
			await ctx.send(f"Could not load {cog}.")
			return
		await ctx.send(f"{cog} loaded.")

	@commands.command(name="unload")
	@commands.is_owner()
	async def unload(self, ctx, cog:str):
		try:
			self.bot.unload_extension(cog)
		except Exception as e:
			await ctx.send(f"Could not unload {cog}.")
			return
		await ctx.send(f"{cog} unloaded.")

	@commands.command(name="reload")
	@commands.is_owner()
	async def reload(self, ctx, cog:str):
		try:
			self.bot.unload_extension(cog)
			self.bot.load_extension(cog)
		except Exception as e:
			await ctx.send(f"Could not reload {cog}.")
			return
		await ctx.send(f"{cog} reloaded.")

def setup(bot):
    bot.add_cog(General(bot))