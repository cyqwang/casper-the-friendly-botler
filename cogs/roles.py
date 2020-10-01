import discord
from discord.ext import tasks, commands

rolesloc = "load/roles.json"
import json
setupfile = open("load/setup.json", "r")
setupdict = json.loads(setupfile.read())
setupfile.close()


class Roles(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.channel = setupdict["channels"]["roles"]

		rolesfile = open(rolesloc, "r")
		self.rolesdict = json.loads(rolesfile.read())
		rolesfile.close()

		self.roles = self.rolesdict["allowed-roles"]
		self.role_message = None
	
	@commands.Cog.listener()
	async def on_ready(self):
		if self.channel is None: pass
		else:
			channel = self.bot.get_channel(self.channel)
			if self.rolesdict["roles-message"] is not None:
				self.role_message = await channel.fetch_message(self.rolesdict["roles-message"])
			else:
				self.role_message = await channel.send(self.roles_text())
				self.rolesdict["roles-message"] = self.role_message.id
				self.commit()
			await self.role_message.pin()

	def commit(self):
		rolesfile = open(rolesloc, "w+")
		self.rolesdict["allowed-roles"] = self.roles
		json.dump(self.rolesdict, rolesfile)
		rolesfile.close()

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot: return
		if message.channel == discord.utils.get(message.guild.text_channels, id=self.channel):
			response = ""

			if message.content[0] == "+":
				role = discord.utils.get(message.guild.roles, name=message.content[1:])
				if role is None:
					response = await message.channel.send(f"I couldn't find the role \"{message.content[1:]}\".")
				elif role.name not in self.roles:
					response = await message.channel.send(f"You do not have permission to add the role \"{message.content[1:]}\".")
				elif role in message.author.roles:
					response = await message.channel.send(f"You already have the role \"{message.content[1:]}\".")
				else:
					await message.author.add_roles(role)
					response = await message.channel.send(f"I've added the role \"{role}\" to you.👻")

			elif message.content[0] == "-":
				role = discord.utils.get(message.guild.roles, name=message.content[1:])
				if role is None:
					response = await message.channel.send(f"I couldn't find the role \"{message.content[1:]}\".")
				elif role not in message.author.roles:
					response = await message.channel.send(f"You don't have the role \"{message.content[1:]}\".")
				else:
					await message.author.remove_roles(role)
					response = await message.channel.send(f"I've removed the role \"{role}\" from you.👻")

			else:
				response = await message.channel.send(f"Sorry, I don't understand.👻")

			await message.delete(delay=2)
			await response.delete(delay=3)

	def roles_text(self):
		text = f"Use +role to add or -role to remove a role.\n\nRoles: \n"

		for role in self.roles:
			text += f"{role} - {self.roles[role]}\n"
		first_role = list(self.roles.keys())[0]
		text += f"Example: +{first_role} or -{first_role}. \n\n"
		return text

	@commands.command(name='role-add')
	@commands.has_role(setupdict["roles"]["resident"])
	async def role_add(self, ctx, role: discord.Role, *, description: str):
		if role.name in self.roles: 
			await ctx.send("This role is already assignable.")
		else:
			self.roles[role.name] = description
			self.commit()
			await self.role_message.edit(content=self.roles_text())
			await ctx.send(f"The role \'{role.name}\' is now assignable.")

	@commands.command(name='role-remove')
	@commands.has_role(setupdict["roles"]["resident"])
	async def role_remove(self, ctx, role: discord.Role):
		if role.name not in self.roles: 
			await ctx.send("This role is already not assignable.")
		else:
			self.roles.pop(role.name)
			self.commit()
			await self.role_message.edit(content=self.roles_text())
			await ctx.send(f"The role \'{role.name}\' is no longer assignable.")

def setup(bot):
    bot.add_cog(Roles(bot))
