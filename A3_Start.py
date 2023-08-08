import os
import discord
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
fname = "memberLogon.csv"

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

#@client.event 
#async def on_ready():

#@client.event
#async def on_member_join(member):

#@client.event
#async def on_member_remove(member):

client.run(TOKEN)