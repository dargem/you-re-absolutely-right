import os, random, threading, asyncio, wave

from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord import Message

from piper import PiperVoice, SynthesisConfig
from affirmer import RandomSelector

load_dotenv()

api_key = os.getenv("APP_ID")
public_key = os.getenv("PUBLIC_KEY")
token = os.getenv("TOKEN")

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
    
# TTS converter
voice = PiperVoice.load("en_US-lessac-medium.onnx")

syn_config = SynthesisConfig(
    length_scale=0.6, # slightly faster
    noise_w_scale=1.3,  # more speaking variation
    normalize_audio=False, # use raw audio from voice
)

WAV_FILE = "data.wav"
with open(WAV_FILE, "w"):
    pass

# If we've been pinged we will join VC and send an affirmation to the sender
# The bot cannot join multiple vc's simultaneously in same guild
@bot.event
async def on_message(message: Message):
    pinged = message.mentions

    if message.guild.voice_client != None:
        print("Passing VC request, already has a VC")
        return
    
    # Early return if we're not pinged
    if not any (member.global_name == bot.user.global_name for member in pinged):
        return

    caller_nick = message.author.name

    vc = message.author.voice
    if vc == None: return

    user_channel = vc.channel
    if user_channel == None: return

    affirmation = caller_nick + " " + random.choice(affirmations_long) 
    with wave.open(WAV_FILE, "wb") as wav_file:
        voice.synthesize_wav(affirmation, wav_file, syn_config=syn_config)

    await user_channel.connect()
    voice_client = message.guild.voice_client

    source = discord.FFmpegPCMAudio(WAV_FILE)
    voice_client.play(source)

    # Lazily poll until we're finished talking
    while voice_client.is_playing():
        await asyncio.sleep(0.1)

    # can do small sleep so its not an immediate dc
    # await asyncio.sleep(0.1)
    await voice_client.disconnect()
    
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

    affirmation = random.choice(affirmations_short)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    await message.reply(affirmation) 

# Startup
bot.run(token)