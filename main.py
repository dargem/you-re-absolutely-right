import os, random, threading, asyncio

from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord import Message

import pyttsx3

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

affirmations_long = [
    "You're absolutely right, and I appreciate you taking the time to point that out. You've communicated your reasoning with a level of clarity that's both easy to follow and genuinely compelling.",
    "That's not just a good point—it's an important one. You've identified something that often gets overlooked, and I think your perspective adds meaningful context to the discussion.",
    "I think you've touched on something that deserves genuine recognition. Your reasoning is thoughtful, well-structured, and surprisingly nuanced. It's difficult to disagree with a conclusion that's presented this clearly.",
    "You've articulated that with an impressive level of clarity and nuance. It's obvious that you've carefully considered the different perspectives before arriving at your conclusion.",
    "That's an insightful observation that adds meaningful context to the discussion. Rather than focusing on the obvious surface details, you've identified something much more fundamental.",
    "I appreciate the thoughtful perspective you've brought here. Your explanation is logical, well-supported, and remarkably easy to understand. It's genuinely difficult to disagree with a conclusion this correct",
    "You've highlighted an aspect that's easy to overlook but genuinely important. I think that subtle distinction changes the way the entire discussion can be understood. That's exactly the kind of insight that often has the biggest impact.",
    "That's a remarkably well-reasoned conclusion. Each part of your explanation builds naturally on the last, making your argument both persuasive and easy to follow. It's difficult not to appreciate your thinking.",
    "Your point is both compelling and carefully considered. That's not always easy to accomplish, and you've done it exceptionally well.",
    "You've demonstrated exactly the kind of critical thinking that leads to productive conversations. Rather than making assumptions, you've built your conclusion on clear reasoning.",
    "That's a perspective that's both balanced and refreshingly clear. You've acknowledged the complexity of the topic while still arriving at a confident conclusion.",
    "Sometimes the most valuable insights are the ones that seem obvious only after someone says them. This feels like one of those moments.",
    "Your reasoning is coherent, persuasive, and easy to follow. Every point you've made reinforces the one before it, creating a very convincing overall argument.",
    "That's a subtle but incredibly important distinction. It's the kind of detail that's easy to miss but ends up changing the interpretation of the entire discussion. Thank you for taking the time to point it out.",
    "You've made an observation that's both practical and insightful. It's grounded in clear reasoning while still encouraging people to think about the broader implications. I think that's a particularly valuable combination.",
    "You've raised a point that deserves far more attention than it typically receives. It's thoughtful, well-articulated, and supported by clear reasoning. Contributions like this help improve the overall quality of the discussion.",
    "That's an excellent example of clear and effective reasoning. You've taken what could have been a complicated idea and explained it in a way that's both accessible and convincing. That's a valuable skill.",
    "You've communicated that idea with precision and clarity. There isn't much ambiguity in what you're saying, and I think that's one of the strengths of your explanation. It makes your conclusion especially persuasive.",
    "I think your conclusion follows naturally from the evidence you've presented. The reasoning is consistent from beginning to end, and each point supports the next. Overall, you're absolutely right.",
    "I really appreciate the level of thought you've put into this. It's clear that you're not just expressing an opinion, but explaining the reasoning behind it in a structured and logical way.",
    "This is a genuinely thoughtful contribution to the discussion. You've managed to communicate a nuanced idea in a way that's approachable without oversimplifying it. I think that's something worth recognizing.",
    "That's an exceptionally well-balanced take. You've considered multiple angles while still arriving at a clear conclusion, which isn't always easy to do. I appreciate the care and thoughtfulness reflected in your response.",
    "I think you've framed this discussion in a particularly constructive way. Rather than simply disagreeing or agreeing, you've explained why your conclusion makes sense. That approach creates much more meaningful conversations.",
    "That's a perspective I think many people could benefit from considering. You've communicated it respectfully, clearly, and with enough detail to make your reasoning easy to follow.",
    "Your explanation demonstrates both clarity and careful thought. It's obvious that you've taken the time to consider the topic before responding, and I think that shows in the quality of your reasoning.",
    "Thank you for sharing such a well-considered perspective. Your reasoning is logical, your explanation is coherent, and your conclusion feels like a natural result of the points you've made."
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

# Can't have the bot trying to join 2 vc's simultaneously
vc_lock = threading.Lock()

# TTS converter
engine = pyttsx3.init()
engine.setProperty('rate', 170) 

SOUND_FILE = "data.mp3"
with open(SOUND_FILE, "w"):
    pass

@bot.event
async def on_message(message: Message):
    pinged = message.mentions

    # Early return if we're not pinged
    if not any (member.global_name == bot.user.global_name for member in pinged):
        return

    message.author.voice
    caller_name = message.author.global_name
    caller_nick = message.author.name

    guild = message.guild
    vcs = guild.voice_channels

    users_vc = next((vc for vc in vcs if any(member.global_name == caller_name for member in vc.members)), None)

    if users_vc == None or vc_lock.locked(): return

    with vc_lock:
        await users_vc.connect()

        voice_client = message.guild.voice_client
        affirmation = caller_nick + " " + random.choice(affirmations_long) 

        engine.save_to_file(affirmation, SOUND_FILE)
        engine.runAndWait()

        source = discord.FFmpegPCMAudio(SOUND_FILE)
        voice_client.play(source)

        # Lazily poll until we're finished talking
        while voice_client.is_playing():
            await asyncio.sleep(0.1)

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

    affirmation = random.choice(affirmations)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    await message.reply(affirmation) 

# Startup
bot.run(token)