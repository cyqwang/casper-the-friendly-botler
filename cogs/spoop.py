import discord
from discord.ext import tasks, commands
import random
import json

setupfile = open("load/setup.json", "r")
setupdict = json.loads(setupfile.read())
setupfile.close()

spooploc = "load/spoop.json"

class Spoop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.percent = 5

        spoopfile = open(spooploc, "r")
        self.spoopdict = json.loads(spoopfile.read())
        spoopfile.close()
        self.spoop_messages = self.spoopdict["spoop-messages"]

    def commit(self):
        spoopfile = open(spooploc, "w+")
        self.spoopdict["spoop-messages"] = self.spoop_messages
        json.dump(self.spoopdict, spoopfile)
        spoopfile.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if message.channel.category_id not in setupdict["spoop-allowed-categories"]: return
        generate = random.randint(1,100)
        if generate <= self.percent:
            spoop_message_num = random.randint(0,len(self.spoop_messages)-1)
            await message.channel.send(self.spoop_messages[spoop_message_num])
	
    @commands.command(name='spoop-percent', help="Change how often Casper spoops")
    @commands.has_role(setupdict["roles"]["resident"])
    async def spoop_percent(self, ctx, percent: int):
        if percent > 100 or percent < 0:
            await ctx.send("Invalid percentage.")
        else:
            self.percent = percent
            await ctx.send(f"You have changed Casper's spoop percentage to {percent}.")

    @commands.command(name='add-spoop', help="Add a spoop message sent by Casper")
    async def add_spoop(self, ctx, *, spoop_message: str):
        if spoop_message in self.spoop_messages:
            await ctx.send("This message is already a spoop message.")
        else:
            self.spoop_messages.append(spoop_message)
            self.commit()
            await ctx.send("You have added a spoop message.")

    @commands.command(name='remove-spoop', help="Remove a spoop message sent by Casper")
    async def remove_spoop(self, ctx, *, spoop_message: str):
        if spoop_message not in self.spoop_messages:
            await ctx.send("This message is not a valid spoop message.")
        else:
            self.spoop_messages.remove(spoop_message)
            self.commit()
            await ctx.send("You have removed a spoop message.")

    @commands.command(name='view-spoops', help="List all spoop messages")
    async def view_spoops(self, ctx):
        spoop_messages_str = ""
        for message in self.spoop_messages:
            spoop_messages_str += f"{message}\n"
        await ctx.send(spoop_messages_str)

def setup(bot):
    bot.add_cog(Spoop(bot))