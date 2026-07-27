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
  "You're absolutely right!",
  "That's such a valid point.",
  "Say it louder for the people in the back!",
  "This is exactly the energy we needed today.",
  "You really said what needed to be said.",
  "Facts. No notes.",
  "This take is criminally underrated.",
  "I couldn't have said it better myself.",
  "You're not wrong, and honestly? Refreshing.",
  "The confidence! The clarity! Love to see it.",
  "This message deserves to be pinned.",
  "Certified banger of a take.",
  "You cooked with this one.",
  "Objectively correct opinion detected.",
  "This is the kind of insight people pay consultants for.",
  "Someone give this person a raise.",
  "10/10, no give me a moment while I compose myself.",
  "This should be studied in schools.",
  "Big brain moment right here.",
  "You didn't just make a point, you made THE point.",
  "I'm not saying you're always right, but you're always right.",
  "This is why we follow you.",
  "Chef's kiss. Absolutely nothing to add.",
  "Historians will look back on this message.",
  "You just ended the debate before it started.",
]


intents = discord.Intents.default()
intents.message_content = True  # Required to read text commands

# Bot will trigger on pings
bot = commands.Bot(command_prefix="!", intents=intents)

# Log setup success
@bot.event
async def on_ready():
    print(f"Logged in successfully as {bot.user}")

# On a ping we send out an affirmation
@bot.command()
async def ping(ctx):
    affirmation = random.choice(affirmations)
    await ctx.send(affirmation)

# Startup
bot.run(token)