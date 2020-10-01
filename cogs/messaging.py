import discord
from discord.ext import tasks, commands

import json
setupfile = open("load/setup.json", "r")
setupdict = json.loads(setupfile.read())
setupfile.close()

class Messaging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
	
    @commands.command(name='say', help="Say something through Casper")
    @commands.has_role(setupdict["roles"]["resident"])
    async def say(self, ctx, channel: discord.TextChannel, *, message: str):
    	#should i check that role has permission to send to this channel??
        await channel.send(message)

    @commands.command(name='edit', help="Edit a message sent by Casper")
    @commands.has_role(setupdict["roles"]["resident"])
    async def edit(self, ctx, channel: discord.TextChannel, message_id: int, *, new_message: str):
    	message = await channel.fetch_message(message_id)
    	await message.edit(content=new_message)
    	await ctx.send("Your message has been edited!")

    @commands.command(name='upload')
    @commands.has_role(setupdict["roles"]["resident"])
    async def upload(self, ctx, channel: discord.TextChannel):
        await channel.send(content = ctx.message.attachments[0].url)

    @commands.command(name='pin')
    @commands.has_role(setupdict["roles"]["resident"])
    async def pin(self, ctx, channel: discord.TextChannel, message_id: int):
        message = await channel.fetch_message(message_id)
        await message.pin()

    @commands.command(name='unpin')
    @commands.has_role(setupdict["roles"]["resident"])
    async def unpin(self, ctx, channel: discord.TextChannel, message_id: int):
        message = await channel.fetch_message(message_id)
        await message.unpin()

    @commands.command(name='react')
    @commands.has_role(setupdict["roles"]["resident"])
    async def react(self, ctx, channel: discord.TextChannel, message_id: int, emoji: str):
        message = await channel.fetch_message(message_id)
        await message.add_reaction(emoji)

    @commands.command(name='unreact')
    @commands.has_role(setupdict["roles"]["resident"])
    async def unreact(self, ctx, channel: discord.TextChannel, message_id: int, user: discord.User, emoji: str):
        message = await channel.fetch_message(message_id)
        await message.remove_reaction(emoji, user)

def setup(bot):
    bot.add_cog(Messaging(bot))