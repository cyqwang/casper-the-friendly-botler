import discord
import datetime
import pytz
import json
import sys
from discord.ext import tasks, commands

RESIDENT_ROLE = "resident"
SCHEDULE = 746387192787501106
GUILD = 494280057871925258
eventsloc = "load/events.json"

class Event:
	@staticmethod
	def parse_event(event_details):
		detail_list = event_details.split(" ")
		event_dict = {"tag":None, "silent":False, "date":202008, "time": 0000, "name":None, "description":None}

		# date_time = datetime.strftime("%m-%d")
		# date_time = datetime.datetime(2020,8,5, tzinfo=pytz.utc)
		return {"tag":"stream", "silent":True, "date_time":2020080000, "name":event_details, "description":"description"}

	@staticmethod
	def make_embed(event_dict, time_zone, guild):
		title_str = f'\N{CALENDAR} {event_dict["name"]} '
		if event_dict["silent"]: title_str += '\N{BELL WITH CANCELLATION STROKE}'
		else: title_str += '\N{BELL}'

		description_str = event_dict["description"]
		if event_dict["tag"] != None: description_str += f'\n#{event_dict["tag"]}'

		#local_time = event_dict["date_time"].astimezone(time_zone)
		#time_str = local_time.strftime("%H:%M %Z on %a, %B %d")
		time_str = "20:00 EST on Tue, Aug 04"

		attendee_str = ">>> "
		num_attendees = len(event_dict["attendees"])
		if num_attendees == 0: attendee_str += "- "
		else:
			for attendee_id in event_dict["attendees"]:
				attendee_str += f'{guild.get_member(attendee_id).mention}\n'
			attendee_str = attendee_str[:-1]

		creator = guild.get_member(event_dict["creator_id"])

		embedVar = discord.Embed(title=title_str, \
								description=description_str, \
								color=0x28e02b)
		embedVar.add_field(name="Time", value=time_str, inline=False)
		embedVar.add_field(name=f"Attendees ({num_attendees})", value=attendee_str, inline=False)
		embedVar.set_footer(text=f'✅ RSVP | 🕐 Convert timezone | Created by {creator.display_name}')	
		return embedVar

class Scheduling(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.channel = SCHEDULE
		self.tz = pytz.timezone("US/Eastern")

		eventsfile = open(eventsloc, "r")
		self.events = json.loads(eventsfile.read())
		eventsfile.close()

	def commit(self):
		eventsfile = open(eventsloc, "w+")
		json.dump(self.events, eventsfile)
		eventsfile.close()

	@commands.command(name = 'ev-create', help="Create an event")
	@commands.has_role(RESIDENT_ROLE)
	async def create(self, ctx, *, event_info: str):
		event_channel = self.bot.get_channel(self.channel)

		event_dict = Event.parse_event(event_info)
		event_dict["creator_id"] = ctx.message.author.id
		event_dict["attendees"] = []
		embedVar = Event.make_embed(event_dict, self.tz, self.bot.get_guild(GUILD))

		event_msg = await event_channel.send(embed=embedVar)
		self.events[event_msg.id] = event_dict

		self.commit()

		await event_msg.add_reaction("\N{WHITE HEAVY CHECK MARK}")
		await event_msg.add_reaction("\N{CLOCK FACE ONE OCLOCK}")

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, reaction_payload):
		event_channel = self.bot.get_channel(self.channel)

		if reaction_payload.member.bot: return	
		if str(reaction_payload.message_id) not in self.events: return
		if reaction_payload.emoji.name != "\N{WHITE HEAVY CHECK MARK}": return
		event_dict = self.events[str(reaction_payload.message_id)]
		event_dict["attendees"].append(reaction_payload.user_id)

		self.commit()

		embedVar = Event.make_embed(event_dict, self.tz, self.bot.get_guild(GUILD))
		event_msg = await event_channel.fetch_message(reaction_payload.message_id)
		await event_msg.edit(embed=embedVar)

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, reaction_payload):
		event_channel = self.bot.get_channel(self.channel)

		user = self.bot.get_user(reaction_payload.user_id)
		if user.bot: return
		if str(reaction_payload.message_id) not in self.events: return
		if reaction_payload.emoji.name != "\N{WHITE HEAVY CHECK MARK}": return
		event_dict = self.events[str(reaction_payload.message_id)]
		event_dict["attendees"].remove(reaction_payload.user_id)

		self.commit()

		embedVar = Event.make_embed(event_dict, self.tz, self.bot.get_guild(GUILD))
		event_msg = await event_channel.fetch_message(reaction_payload.message_id)
		await event_msg.edit(embed=embedVar)
	#we want to DM the user, ask what time zone they want, then say when
	# @commands.Cog.listener()
	# async def on_reaction_add(self, reaction, user):
	# 	if user.bot: return		
	# 	if reaction.message.id not in self.events: return
	# 	if reaction.emoji != "\N{CLOCK FACE ONE OCLOCK}": return

	#edit event, give the message ID of the event

	# @tasks.loop(seconds=5.0)
	# async def time_check():
	# 	now = datetime.strftime(datetime.now(), f)
	# 	await 

# class Calendar:
# 	def __init__(self, creator, tag = None, message = None, auto_update = False):
# 		self.creator = creator
# 		self.tag = tag
# 		self.message = message
# 		self.auto_update = auto_update

# 	@staticmethod
# 	def parse_calendar(event_details):
# 		# detail_list = event_details.split(" ")
# 		# if(detail_list[0])
# 		# date_time = datetime.strftime("%m-%d")
# 		date_time = datetime.datetime(2020,8,5, tzinfo=pytz.utc)
# 		return {"tag":"stream", "silent":True, "date_time":date_time, "name":"name", "description":"description"}

# 	@staticmethod
# 	def parse_embed(message, embed):

# 	def make_embed(self, time_zone):
# 		return embedVar

def setup(bot):
    bot.add_cog(Scheduling(bot))