import os, asyncio, wave, tempfile

from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord import Message, Guild, RawReactionActionEvent

from collections import defaultdict
from affirmer import Affirmer
from spam_buffer import SpamBuffer, PushResult
from pathlib import Path
from TTS import PiedPierTTS
from logger import Logger, Level

load_dotenv()

api_key = os.getenv("APP_ID")
public_key = os.getenv("PUBLIC_KEY")
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Required to read text commands

# Bot will trigger on pings
bot = commands.Bot(command_prefix="!", intents=intents)

logger = Logger()

# Log setup success
@bot.event
async def on_ready():
    logger.log(Level.INFO, f"Logged in successfully as {bot.user}")
    logger.log(Level.INFO, f"Connected to {len(bot.guilds)} guilds:")
    for guild in bot.guilds:
        logger.log(Level.INFO, f" - {guild.name} (ID: {guild.id})")

guild_affirmers: defaultdict[Guild, Affirmer] = defaultdict(lambda: Affirmer(PiedPierTTS()))

# If we've been pinged we will join VC and send an affirmation to the sender
# The bot cannot join multiple vc's simultaneously in same guild
@bot.event
async def on_message(message: Message):
    pinged = message.mentions

    if message.guild.voice_client != None:
        # For now we just skip it, could consider something like a job queue?
        # Would likely result in very bad latency though in those cases and would have to check for spam
        logger.log(Level.WARNING, "Passing VC request, already has a VC")
        return
    
    # Early return if we're not pinged
    if not any (member.global_name == bot.user.global_name for member in pinged):
        return

    name = message.author.name

    vc = message.author.voice
    if vc == None: return

    user_channel = vc.channel
    if user_channel == None: return

    # Create a tempfile to play our audio in
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp:
        guild_affirmers[message.guild].write_voice(name, Path(temp.name))
        source = discord.FFmpegPCMAudio(temp.name)

        voice_client = await user_channel.connect()
        
        # Use an event to wait for the audio to finish
        done = asyncio.Event()
        def after_playing(error):
            if error:
                logger.log(Level.ERROR, f"Player error: {error}")
            bot.loop.call_soon_threadsafe(done.set)

        voice_client.play(source, after=after_playing)

        await done.wait()

        if message.guild.voice_client:
            await voice_client.disconnect()

# Used to filter spam
spam_buffer = SpamBuffer(logger)

# On a reaction we send out an affirmation
@bot.event
async def on_raw_reaction_add(payload: RawReactionActionEvent):
    # Ignore the bot's own reactions
    if payload.user_id == bot.user.id:
        return

    logger.log(Level.DEBUG, f"Triggered by {payload.emoji}")

    # Check for the 100 emoji
    if str(payload.emoji) != "💯":
        return


    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    name = message.author.name

    PushResult: PushResult = spam_buffer.add(name)

    match(PushResult):
        case PushResult.FAIL: 
            logger.log(Level.WARNING, f"Ignored user {name} after spam was detected")
            return
        case PushResult.SUCCESS: pass
        case PushResult.SUCCESS_REACHED_MAX: 
            # Rate limit comment
            logger.log(Level.WARNING, f"Gave user {name} rate limit response")
            await message.reply(f"This is such a brilliant point, I need some time to stew over this {name}.")
            return

    affirmation = guild_affirmers[payload.member.guild].get_short(name)
    await message.reply(affirmation) 

# Startup
bot.run(token)