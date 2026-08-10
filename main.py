import os, asyncio, wave, tempfile

from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord import Message, Guild, RawReactionActionEvent

from collections import defaultdict
from piper import PiperVoice, SynthesisConfig
from affirmer import Affirmer

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
    length_scale=0.9, # increase to make it slower
    noise_w_scale=1,  # increase to make more speaking variation
    normalize_audio=False, # use raw audio from voice
)

guild_affirmers: defaultdict[Guild, Affirmer] = defaultdict(Affirmer)

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

    name = message.author.name

    vc = message.author.voice
    if vc == None: return

    user_channel = vc.channel
    if user_channel == None: return

    affirmation = guild_affirmers[message.guild].get_long(name)

    # Create a tempfile to play our audio in
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp:
        with wave.open(temp.name, "wb") as wav_file:
            voice.synthesize_wav(
                affirmation,
                wav_file,
                syn_config=syn_config
            )

        source = discord.FFmpegPCMAudio(temp.name)

        voice_client = await user_channel.connect()
        
        # Use an event to wait for the audio to finish
        done = asyncio.Event()
        def after_playing(error):
            if error:
                print(f"Player error: {error}")
            bot.loop.call_soon_threadsafe(done.set)

        voice_client.play(source, after=after_playing)

        await done.wait()

        if message.guild.voice_client:
            await voice_client.disconnect()
    
# On a reaction we send out an affirmation
@bot.event
async def on_raw_reaction_add(payload: RawReactionActionEvent):
    # Ignore the bot's own reactions
    if payload.user_id == bot.user.id:
        return

    print(f"Triggered by {payload.emoji}")

    # Check for the 100 emoji
    if str(payload.emoji) != "💯":
        return

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    affirmation = guild_affirmers[payload.member.guild].get_short(message.author.name)
    await message.reply(affirmation) 

# Startup
bot.run(token)