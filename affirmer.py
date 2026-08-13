from selector import RandomSelector
from pydub import AudioSegment
from threading import Lock
from pathlib import Path

NAME_REPLACEMENT_SYM = "%"

affirmations_short = [
    f"You're absolutely right, {NAME_REPLACEMENT_SYM}, and I appreciate you taking the time to point that out.",
    "That's not just a good point — it's an important one.",
    "I think you've touched on something that deserves genuine recognition.",
    "You've articulated that with an impressive level of clarity and nuance.",
    "That's an insightful observation that adds meaningful context to the discussion.",
    f"I appreciate the thoughtful perspective you've brought here, {NAME_REPLACEMENT_SYM}.",
    "You've highlighted an aspect that's easy to overlook but genuinely important.",
    "That's a remarkably well-reasoned conclusion.",
    "Your point is both compelling and carefully considered.",
    "You've demonstrated exactly the kind of critical thinking that leads to productive conversations.",
    "That's a perspective that's both balanced and refreshingly clear.",
    f"I think you've captured the heart of the issue exceptionally well, {NAME_REPLACEMENT_SYM}.",
    "Your reasoning is coherent, persuasive, and easy to follow.",
    "That's a subtle but incredibly important distinction.",
    "You've made an observation that's both practical and insightful.",
    "I genuinely appreciate the depth of thought reflected in your response.",
    "You've raised a point that deserves far more attention than it typically receives.",
    f"That's an excellent example of clear and effective reasoning, {NAME_REPLACEMENT_SYM}.",
    "You've communicated that idea with precision and clarity.",
    "I think your conclusion follows naturally from the evidence you've presented.",
    "That's not just correct — it's exceptionally well put.",
    "You've hit on something important here — and explained it beautifully.",
    "I want to acknowledge how clearly you've laid that out.",
    "That's a genuinely sharp distinction — one most people would miss entirely.",
    f"You're not wrong, {NAME_REPLACEMENT_SYM} — in fact, you're precisely right.",
    "That's a fantastic point, and it deserves to be sat with for a moment.",
    "I think that's an exceptionally clear way of framing it — well done.",
    "You've cut right to the core of the issue — and done it elegantly.",
    "That's a genuinely valuable contribution to this conversation.",
    f"I appreciate how precisely you've reasoned through that, {NAME_REPLACEMENT_SYM}.",
    "You've made a compelling case — one that's hard to argue with.",
    "That's an important nuance — and you've explained it exceptionally well.",
    "I think it's worth pausing to recognize how well-constructed that argument is.",
    "You're absolutely correct — and remarkably articulate about it too.",
    f"That's a genuinely thoughtful take, {NAME_REPLACEMENT_SYM} — one that adds real clarity here.",
]

affirmations_long = [
    f"You're absolutely right, {NAME_REPLACEMENT_SYM}, and honestly, that was one of the clearest, most well-reasoned points I've ever seen someone make in a conversation like this.",
    f"Wow, incredible point, {NAME_REPLACEMENT_SYM}, genuinely one of the best I've heard. I'm genuinely not sure anyone else could have said that better.",
    f"That's exactly right, {NAME_REPLACEMENT_SYM}, and honestly? Beautifully put too. I really don't think it could have been phrased any better than that.",
    f"I have to say, {NAME_REPLACEMENT_SYM}, that's a fantastic observation you just made there. You really nailed it there, and it shows in every word.",
    f"You're spot on with that, {NAME_REPLACEMENT_SYM}, no question about it at all. That kind of clarity is rare and honestly genuinely impressive to witness.",
    f"That's a brilliant way to put it, {NAME_REPLACEMENT_SYM}, seriously well done there. No notes whatsoever, truly an excellent and thoughtful point overall.",
    f"Absolutely correct, {NAME_REPLACEMENT_SYM}, and remarkably well said if I'm being honest. Love to see that kind of clear thinking on display.",
    f"That's such a great point, {NAME_REPLACEMENT_SYM}, genuinely one of your best yet! You really have a gift for explaining things this well.",
    f"You couldn't be more right about that, {NAME_REPLACEMENT_SYM}, not even a little. That was genuinely such a pleasure to sit here and listen to.",
    f"Incredible insight, {NAME_REPLACEMENT_SYM}. Truly one of the sharpest takes I've seen — that's exactly the right way to look at the whole thing.",
    f"That's 100% correct, {NAME_REPLACEMENT_SYM}, no doubt about it in my mind. And impressively articulated too, which honestly makes it even better.",
    f"You nailed it completely, {NAME_REPLACEMENT_SYM}, there's really nothing left to add here. That was a truly outstanding and well-constructed point overall.",
    f"That's a fantastic take, {NAME_REPLACEMENT_SYM}, genuinely one of the better ones today. And honestly, very well argued from start to finish too.",
    f"You're totally right about that, {NAME_REPLACEMENT_SYM}, and it's not even close. Genuinely great thinking there, the kind that stands out immediately.",
    f"That's exactly it, {NAME_REPLACEMENT_SYM}. You've really summed it up perfectly there — I'm consistently impressed by how clearly you manage to explain things.",
    f"Perfectly said, {NAME_REPLACEMENT_SYM}, and completely accurate from beginning to end honestly. Truly excellent work, seriously one of your best moments yet.",
    f"That's such a sharp point, {NAME_REPLACEMENT_SYM}, genuinely impressive stuff right there. You clearly know exactly what you're talking about, no question.",
    f"You're right on the money with that one, {NAME_REPLACEMENT_SYM}, completely spot on. That was wonderfully explained too, genuinely a pleasure to hear.",
    f"That's a genuinely great observation, {NAME_REPLACEMENT_SYM}, one of the better ones honestly. Impressively clear and completely correct, truly nothing more to add.",
    f"Couldn't agree more with you on that, {NAME_REPLACEMENT_SYM}, not even slightly. And that was a fantastic way to explain such a tricky idea.",
    f"That's absolutely correct, {NAME_REPLACEMENT_SYM}, no doubt in my mind whatsoever. And honestly kind of a brilliant point when you think about it.",
    f"You're right, {NAME_REPLACEMENT_SYM}, as usual, honestly at this point it's expected. Truly impressive reasoning there, seriously well done once again.",
    f"That's a wonderful point, {NAME_REPLACEMENT_SYM}, genuinely one of the better ones lately. And remarkably well put together, truly a pleasure to hear.",
    f"Spot on, {NAME_REPLACEMENT_SYM}, completely and totally spot on if I'm honest. That's exactly the kind of insight that really stands out here.",
    f"You're completely right about that, {NAME_REPLACEMENT_SYM}, genuinely no argument from me. And that was genuinely well said, truly impressive stuff overall.",
    f"That's a fantastic conclusion, {NAME_REPLACEMENT_SYM}, seriously one of the better ones today. Really well reasoned, truly, genuinely nothing left to critique here.",
]

affirmations_bombastic = [
    f"Let me tell you something, {NAME_REPLACEMENT_SYM} — I've heard a lot of ideas in my life, a tremendous number of ideas, believe me, and this one, this one right here, is the best. Nobody's ever said it better. Nobody.",
    f"{NAME_REPLACEMENT_SYM}, that's incredible, it really is, people are going to be talking about that point for a long time, a very long time, maybe the longest time anybody's ever talked about anything, honestly.",
    f"Nobody — and I mean absolutely nobody — explains it like {NAME_REPLACEMENT_SYM} just did. Tremendous clarity, the best clarity anyone's ever seen, and a lot of very smart people agree with me on this, a lot.",
    f"That's a great point, {NAME_REPLACEMENT_SYM}, one of the greatest points I've ever heard in my entire life, and I've heard plenty of points, believe me, plenty, and this one beats them all. It's not even close, frankly, it's a landslide.",
    f"Everybody's saying it, {NAME_REPLACEMENT_SYM}, everybody — that was one of the smartest things said all day, maybe all year, maybe ever, some people are calling it historic, and honestly, they might be right.",
    f"{NAME_REPLACEMENT_SYM}, incredible stuff, just incredible, some people call it genius, I call it genius too, we're all calling it genius, it's genius, there's no other word for it, just genius",
    f"You know what, {NAME_REPLACEMENT_SYM}, that's exactly right, one hundred percent right, and frankly, nobody explains things better than you do, nobody, not even close, it's not even a competition at this point.",
    f"That's the best point I've heard all week, {NAME_REPLACEMENT_SYM}, maybe the best point I've heard all month, and believe me, I hear a lot of points, a tremendous number of points, and yours is the best.",
    f"{NAME_REPLACEMENT_SYM}, tremendous insight, absolutely tremendous, the likes of which we haven't seen in a long time, maybe ever, people are going to remember this moment, mark my words.",
    f"Total winner of a point right there, {NAME_REPLACEMENT_SYM}, a total winner, a champion of a point really, everybody agrees, everybody, there's no disagreement here, none whatsoever.",
]

WAV_CACHE = "wav_cache"

cache_lock = Lock()

# Very simple storage, name of file is == TTS it speaks out. 

# We have a "cache" where if text is the name of a file,
# we can reuse the file by concatenating it
def get_TTS(text: str) -> str:
    with cache_lock:
        for file in Path(WAV_CACHE).iterdir():
            if file.name == text:
                return file.name

    # We have not found it in our cache, so we need to generate it

# Generates affirmations  
class Affirmer:
    def __init__(self):
        self.short = RandomSelector(affirmations_short)
        self.long = RandomSelector(affirmations_bombastic)

    def get_text(self, name: str) -> str:
        return self.short.choose().replace(NAME_REPLACEMENT_SYM, name)

    # Write a voice to the given file
    def write_voice(self, voice: str, filename: str) -> None:
        affirmation = self.long.choose()

        # The affirmation does not have to have a name
        # We expect it to be length 1 (no name) or length 2 (name in middle)
        parts = affirmation.split(NAME_REPLACEMENT_SYM)



        
