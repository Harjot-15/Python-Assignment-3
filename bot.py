import os
import discord
import csv
import logging
from dotenv import load_dotenv
from datetime import datetime

logging.basicConfig(level=logging.INFO)

# Loads environment variables from the Info.env file
load_dotenv("Info.env")
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
fname = "Friends.csv"  # Filename for the CSV where member data will be stored

# Set up the necessary intents to monitor members joining and leaving
intents = discord.Intents.default()
intents.members = True

# Initialize the Discord client with the specified intents
client = discord.Client(intents=intents)

def is_member_in_csv(member_name):
    """Check if a member is already present in the CSV."""
    with open(fname, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 0 and row[0] == member_name:
                return True
    return False

@client.event 
async def on_ready():
    """Event triggered when the bot is ready."""
    logging.info("Bot is ready.")
    # If the CSV file doesn't exist, create it and populate with current members of the server
    if not os.path.exists(fname):
        with open(fname, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Date Joined"])
            guild = discord.utils.get(client.guilds, name=GUILD)
            for member in guild.members:
                writer.writerow([member.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

@client.event
async def on_member_join(member):
    """Event triggered when a new member joins the server."""
    logging.info(f"Member joined: {member.name}")
    # If the joining member is not already in the CSV, add their information
    if not is_member_in_csv(member.name):
        with open(fname, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([member.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

@client.event
async def on_member_remove(member):
    """Event triggered when a member leaves or is removed from the server."""
    logging.info(f"Member left: {member.name}")
    rows = []
    # Reads the current entries from the CSV
    with open(fname, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 0 and row[0] != member.name:
                rows.append(row)
    # Writes the updated list back to the CSV, excluding the member who left
    with open(fname, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

# Start the bot using the provided token
client.run(TOKEN)
