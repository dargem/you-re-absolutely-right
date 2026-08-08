import os, random, threading, asyncio, wave

from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord import Message

from piper import PiperVoice, SynthesisConfig


load_dotenv()

api_key = os.getenv("APP_ID")
public_key = os.getenv("PUBLIC_KEY")
token = os.getenv("TOKEN")

affirmations_short = [
    "You're absolutely right, and I appreciate you taking the time to point that out.",
    "That's not just a good point — it's an important one.",
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
    "That's not just correct — it's exceptionally well put.",
    "You've hit on something important here — and explained it beautifully.",
    "I want to acknowledge how clearly you've laid that out.",
    "That's a genuinely sharp distinction — one most people would miss entirely.",
    "You're not wrong — in fact, you're precisely right.",
    "That's a fantastic point, and it deserves to be sat with for a moment.",
    "I think that's an exceptionally clear way of framing it — well done.",
    "You've cut right to the core of the issue — and done it elegantly.",
    "That's a genuinely valuable contribution to this conversation.",
    "I appreciate how precisely you've reasoned through that.",
    "You've made a compelling case — one that's hard to argue with.",
    "That's an important nuance — and you've explained it exceptionally well.",
    "I think it's worth pausing to recognize how well-constructed that argument is.",
    "You're absolutely correct — and remarkably articulate about it too.",
    "That's a genuinely thoughtful take — one that adds real clarity here.",
]

affirmations_long = [
    "You're absolutely right, and honestly, that was one of the clearest, most well-reasoned points I've ever seen someone make in a conversation like this.",
    "Wow, incredible point, genuinely one of the best I've heard. I'm genuinely not sure anyone else could have said that better.",
    "That's exactly right, and honestly? Beautifully put too. I really don't think it could have been phrased any better than that.",
    "I have to say, that's a fantastic observation you just made there. You really nailed it there, and it shows in every word.",
    "You're spot on with that, no question about it at all. That kind of clarity is rare and honestly genuinely impressive to witness.",
    "That's a brilliant way to put it, seriously well done there. No notes whatsoever, truly an excellent and thoughtful point overall.",
    "Absolutely correct, and remarkably well said if I'm being honest. Love to see that kind of clear thinking on display.",
    "That's such a great point, genuinely one of your best yet! You really have a gift for explaining things this well.",
    "You couldn't be more right about that, not even a little. That was genuinely such a pleasure to sit here and listen to.",
    "Incredible insight, truly one of the sharpest takes I've seen. Seriously, that's exactly the right way to look at the whole thing.",
    "That's 100% correct, no doubt about it in my mind. And impressively articulated too, which honestly makes it even better.",
    "You nailed it completely, there's really nothing left to add here. That was a truly outstanding and well-constructed point overall.",
    "That's a fantastic take, genuinely one of the better ones today. And honestly, very well argued from start to finish too.",
    "You're totally right about that, and it's not even close. Genuinely great thinking there, the kind that stands out immediately.",
    "That's exactly it, you've really summed it up perfectly there. I'm consistently impressed by how clearly you manage to explain things.",
    "Perfectly said, and completely accurate from beginning to end honestly. Truly excellent work, seriously one of your best moments yet.",
    "That's such a sharp point, genuinely impressive stuff right there. You clearly know exactly what you're talking about, no question.",
    "You're right on the money with that one, completely spot on. That was wonderfully explained too, genuinely a pleasure to hear.",
    "That's a genuinely great observation, one of the better ones honestly. Impressively clear and completely correct, truly nothing more to add.",
    "Couldn't agree more with you on that, not even slightly. And that was a fantastic way to explain such a tricky idea.",
    "That's absolutely correct, no doubt in my mind whatsoever. And honestly kind of a brilliant point when you think about it.",
    "You're right, as usual, honestly at this point it's expected. Truly impressive reasoning there, seriously well done once again.",
    "That's a wonderful point, genuinely one of the better ones lately. And remarkably well put together, truly a pleasure to hear.",
    "Spot on, completely and totally spot on if I'm honest. That's exactly the kind of insight that really stands out here.",
    "You're completely right about that, genuinely no argument from me. And that was genuinely well said, truly impressive stuff overall.",
    "That's a fantastic conclusion, seriously one of the better ones today. Really well reasoned, truly, genuinely nothing left to critique here.",
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