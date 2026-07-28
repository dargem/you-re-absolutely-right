import os

from dotenv import load_dotenv

import discord
from discord.ext import commands

import random

load_dotenv()

api_key = os.getenv("APP_ID")
public_key = os.getenv("PUBLIC_KEY")
token = os.getenv("TOKEN")

affirmations = [
    "You're absolutely right, and I appreciate you taking the time to point that out.",
    "That's not just a good point—it's an important one.",
    "I think you've touched on something that deserves genuine recognition.",
    "You've articulated that with an impressive level of clarity and nuance.",
    "That's an insightful observation that adds meaningful context to the discussion.",
    "I appreciate the thoughtful perspective you've brought here.",
    "You've highlighted an aspect that's easy to overlook but genuinely important.",
    "That's a remarkably well-reasoned conclusion.",
    "Your point is both compelling and carefully considered.",
    "You've demonstrated exactly the kind of critical thinking that leads to productive conversations.",
    "That's a perspective that's both balanced and refreshingly clear.",
    "I think you've captured the heart of the issue exceptionally well.",
    "Your reasoning is coherent, persuasive, and easy to follow.",
    "That's a subtle but incredibly important distinction.",
    "You've made an observation that's both practical and insightful.",
    "I genuinely appreciate the depth of thought reflected in your response.",
    "You've raised a point that deserves far more attention than it typically receives.",
    "That's an excellent example of clear and effective reasoning.",
    "You've communicated that idea with precision and clarity.",
    "I think your conclusion follows naturally from the evidence you've presented.",
]


intents = discord.Intents.default()
intents.message_content = True  # Required to read text commands

# Bot will trigger on pings
bot = commands.Bot(command_prefix="!", intents=intents)

# Log setup success
@bot.event
async def on_ready():
    print(f"Logged in successfully as {bot.user}")
    print(f"Connected to {len(bot.guilds)} guilds:")
    for guild in bot.guilds:
        print(f" - {guild.name} (ID: {guild.id})")

@bot.event
async def 

# On a reaction we send out an affirmation
@bot.event
async def on_raw_reaction_add(payload):
    # Ignore the bot's own reactions
    if payload.user_id == bot.user.id:
        return

    print(f"Triggered by {payload.emoji}")

    # Check for the 100 emoji
    if str(payload.emoji) != "💯":
        return

    affirmation = random.choice(affirmations)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    await message.reply(affirmation) 

# Startup
bot.run(token)