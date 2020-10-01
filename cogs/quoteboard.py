import discord
from discord.ext import tasks, commands

import json
setupfile = open("load/setup.json", "r")
setupdict = json.loads(setupfile.read())
setupfile.close()

class Quoteboard(commands.Cog):
	#add check that the view permissions of the message >= view permissions of quote-board
	def __init__(self, bot):
		self.bot = bot
		self.reaction = "\N{WHITE MEDIUM STAR}"
		self.min_react = 1
		self.channel = setupdict["channels"]["quote-board"]
		self.starred_messages = {}

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		if reaction.emoji != self.reaction: return
		message = reaction.message
		quote_channel = self.bot.get_channel(self.channel)

		if reaction.count >= self.min_react:
			embedVar = discord.Embed(
									description=f'[View Message]({message.jump_url})\n \
									{message.content}',\
									color=0x994BEA)
			embedVar.set_author(name=f'{message.author.name} in #{message.channel}', icon_url=message.author.avatar_url)
			embedVar.set_footer(text=f'{reaction.count}{self.reaction} | {message.created_at.date()}')
			if message.id in self.starred_messages:
				await self.starred_messages[message.id].edit(embed=embedVar)
			else:
				self.starred_messages[message.id] = await quote_channel.send(embed=embedVar)

	@commands.Cog.listener()
	async def on_reaction_remove(self, reaction, user):
		if (reaction.emoji != self.reaction): return

		message = reaction.message
		quote_channel = self.bot.get_channel(self.channel)

		if reaction.count < self.min_react:
			star_msg = self.starred_messages.pop(message.id, None)
			await star_msg.delete()
		else:
			embedVar = discord.Embed(title=f'{message.author.name} in #{message.channel}', \
									description=f"[View Message]({message.jump_url})\n \
									{message.content}", \
									color=0x994BEA)
			embedVar.set_author(name=f'{message.author.name} in #{message.channel}', icon_url=message.author.avatar_url)
			embedVar.set_footer(text=f'{reaction.count}{self.reaction} | {message.created_at.date()}')
			await self.starred_messages[message.id].edit(embed=embedVar)

	# @commands.Cog.listener()
	# async def on_raw_reaction_remove(self, reaction_payload):
	# 	print("here")
	# 	if (reaction_payload.emoji.name != self.reaction): return

	# 	message = await self.bot.get_channel(reaction_payload.channel_id).fetch_message(reaction_payload.message_id)
	# 	quote_channel = self.bot.get_channel(self.channel)

	# 	reaction = discord.utils.get(message.reactions, emoji = reaction_payload.emoji)
	#	always returns None....

	# 	if reaction == None or reaction.count < self.min_react:
	# 		star_msg = self.starred_messages.pop(message.id, None)
	# 		await star_msg.delete()
	# 	else:
	# 		embedVar = discord.Embed(title=f'{message.author.name} in #{message.channel}', \
	# 								description=f"[View Message]({message.jump_url})\n \
	# 								{message.content}", \
	# 								color=0x994BEA)
	# 		embedVar.set_author(name=f'{message.author.name} in #{message.channel}', icon_url=message.author.avatar_url)
	# 		embedVar.set_footer(text=f'{reaction.count}{self.reaction} | {message.created_at.date()}')
	# 		await self.starred_messages[message.id].edit(embed=embedVar)

	@commands.command(name = 'qb-minimum', help="Set minimum star count for quote-board")
	@commands.has_role(setupdict["roles"]["resident"])
	async def qb_minimum(self, ctx, num_stars: int):
		self.min_react = num_stars
		await ctx.send(f"You have set the star minimum to {num_stars} stars.")

	@commands.command(name = 'qb-emoji', help="Set emoji for quote-board")
	@commands.has_role(setupdict["roles"]["resident"])
	async def qb_emoji(self, ctx, emoji: str):
		self.reaction = emoji
		await ctx.send(f"You have set the quote-board emoji to {emoji}.")

def setup(bot):
    bot.add_cog(Quoteboard(bot))