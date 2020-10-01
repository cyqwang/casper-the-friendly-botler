import discord
from discord.ext import tasks, commands
import json

RESIDENT_ROLE = "resident"

shoppingloc = "load/shopping.json"

class House(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        shoppingfile = open(shoppingloc, "r")
        self.shopping_list = json.loads(shoppingfile.read())
        shoppingfile.close()

    def commit(self):
        shoppingfile = open(shoppingloc, "w+")
        json.dump(self.shopping_list, shoppingfile)
        shoppingfile.close()
	
    @commands.command(name='shopping-list', help="View shopping list")
    @commands.has_role(RESIDENT_ROLE)
    async def shopping_list(self, ctx):
        shopping_str = ""
        for store in self.shopping_list:
            if len(self.shopping_list[store]) == 0: pass
            shopping_str += (f"**{store}**\n")
            for item in self.shopping_list[store]:
                shopping_str+=f"{item}\n"
            shopping_str +="\n"
        await ctx.send(shopping_str[:-1])

    @commands.command(name='shopping-add', help="Add items to the shopping list")
    @commands.has_role(RESIDENT_ROLE)
    async def shopping_add(self, ctx, *, items_str: str):
        items = items_str.split(", ")
        category = "Uncategorized"
        if items[0] in self.shopping_list:
            category = items[0]
            items = items[1:]
        self.shopping_list[category] += items[1:]
        self.commit()
        await ctx.send("You have successfully added to the shopping list.")

    @commands.command(name='shopping-remove', help="Remove items from the shopping list")
    @commands.has_role(RESIDENT_ROLE)
    async def shopping_remove(self, ctx, *, items_str: str):
        items = items_str.split(", ")
        in_list = ""
        not_in_list = ""
        category = "Uncategorized"
        if items[0] in self.shopping_list:
            category = items[0]
            items = items[1:]
        for item in items:
            if item in self.shopping_list[category]:
                in_list += f"{item}, "
                self.shopping_list[category].remove(item)
            else:
                not_in_list += f"{item}, "
        self.commit()
        await ctx.send(f"You have successfully removed {in_list} from {category}. We could not find {not_in_list}.")

    @commands.command(name='shopping-clear', help="Clears the shopping list")
    async def shopping_clear(self, ctx, store: str=None, *, items):
        spoop_messages_str = ""
        for message in self.spoop_messages:
            spoop_messages_str += f"{message}\n"
        await ctx.send(spoop_messages_str)

def setup(bot):
    bot.add_cog(House(bot))