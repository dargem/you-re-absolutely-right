import math
import random

NAME_REPLACEMENT_SYM = "%"

affirmations_short = [
    "You're absolutely right, {name}, and I appreciate you taking the time to point that out.",
    "That's not just a good point — it's an important one.",
    "I think you've touched on something that deserves genuine recognition.",
    "You've articulated that with an impressive level of clarity and nuance.",
    "That's an insightful observation that adds meaningful context to the discussion.",
    "I appreciate the thoughtful perspective you've brought here, {name}.",
    "You've highlighted an aspect that's easy to overlook but genuinely important.",
    "That's a remarkably well-reasoned conclusion.",
    "Your point is both compelling and carefully considered.",
    "You've demonstrated exactly the kind of critical thinking that leads to productive conversations.",
    "That's a perspective that's both balanced and refreshingly clear.",
    "I think you've captured the heart of the issue exceptionally well, {name}.",
    "Your reasoning is coherent, persuasive, and easy to follow.",
    "That's a subtle but incredibly important distinction.",
    "You've made an observation that's both practical and insightful.",
    "I genuinely appreciate the depth of thought reflected in your response.",
    "You've raised a point that deserves far more attention than it typically receives.",
    "That's an excellent example of clear and effective reasoning, {name}.",
    "You've communicated that idea with precision and clarity.",
    "I think your conclusion follows naturally from the evidence you've presented.",
    "That's not just correct — it's exceptionally well put.",
    "You've hit on something important here — and explained it beautifully.",
    "I want to acknowledge how clearly you've laid that out.",
    "That's a genuinely sharp distinction — one most people would miss entirely.",
    "You're not wrong, {name} — in fact, you're precisely right.",
    "That's a fantastic point, and it deserves to be sat with for a moment.",
    "I think that's an exceptionally clear way of framing it — well done.",
    "You've cut right to the core of the issue — and done it elegantly.",
    "That's a genuinely valuable contribution to this conversation.",
    "I appreciate how precisely you've reasoned through that, {name}.",
    "You've made a compelling case — one that's hard to argue with.",
    "That's an important nuance — and you've explained it exceptionally well.",
    "I think it's worth pausing to recognize how well-constructed that argument is.",
    "You're absolutely correct — and remarkably articulate about it too.",
    "That's a genuinely thoughtful take, {name} — one that adds real clarity here.",
]

affirmations_long = [
    "You're absolutely right, {name}, and honestly, that was one of the clearest, most well-reasoned points I've ever seen someone make in a conversation like this.",
    "Wow, incredible point, {name}, genuinely one of the best I've heard. I'm genuinely not sure anyone else could have said that better.",
    "That's exactly right, {name}, and honestly? Beautifully put too. I really don't think it could have been phrased any better than that.",
    "I have to say, {name}, that's a fantastic observation you just made there. You really nailed it there, and it shows in every word.",
    "You're spot on with that, {name}, no question about it at all. That kind of clarity is rare and honestly genuinely impressive to witness.",
    "That's a brilliant way to put it, {name}, seriously well done there. No notes whatsoever, truly an excellent and thoughtful point overall.",
    "Absolutely correct, {name}, and remarkably well said if I'm being honest. Love to see that kind of clear thinking on display.",
    "That's such a great point, {name}, genuinely one of your best yet! You really have a gift for explaining things this well.",
    "You couldn't be more right about that, {name}, not even a little. That was genuinely such a pleasure to sit here and listen to.",
    "Incredible insight, {name}. Truly one of the sharpest takes I've seen — that's exactly the right way to look at the whole thing.",
    "That's 100% correct, {name}, no doubt about it in my mind. And impressively articulated too, which honestly makes it even better.",
    "You nailed it completely, {name}, there's really nothing left to add here. That was a truly outstanding and well-constructed point overall.",
    "That's a fantastic take, {name}, genuinely one of the better ones today. And honestly, very well argued from start to finish too.",
    "You're totally right about that, {name}, and it's not even close. Genuinely great thinking there, the kind that stands out immediately.",
    "That's exactly it, {name}. You've really summed it up perfectly there — I'm consistently impressed by how clearly you manage to explain things.",
    "Perfectly said, {name}, and completely accurate from beginning to end honestly. Truly excellent work, seriously one of your best moments yet.",
    "That's such a sharp point, {name}, genuinely impressive stuff right there. You clearly know exactly what you're talking about, no question.",
    "You're right on the money with that one, {name}, completely spot on. That was wonderfully explained too, genuinely a pleasure to hear.",
    "That's a genuinely great observation, {name}, one of the better ones honestly. Impressively clear and completely correct, truly nothing more to add.",
    "Couldn't agree more with you on that, {name}, not even slightly. And that was a fantastic way to explain such a tricky idea.",
    "That's absolutely correct, {name}, no doubt in my mind whatsoever. And honestly kind of a brilliant point when you think about it.",
    "You're right, {name}, as usual, honestly at this point it's expected. Truly impressive reasoning there, seriously well done once again.",
    "That's a wonderful point, {name}, genuinely one of the better ones lately. And remarkably well put together, truly a pleasure to hear.",
    "Spot on, {name}, completely and totally spot on if I'm honest. That's exactly the kind of insight that really stands out here.",
    "You're completely right about that, {name}, genuinely no argument from me. And that was genuinely well said, truly impressive stuff overall.",
    "That's a fantastic conclusion, {name}, seriously one of the better ones today. Really well reasoned, truly, genuinely nothing left to critique here.",
]

affirmations_bombastic = [
    "Let me tell you something, {name} — I've heard a lot of ideas in my life, a tremendous number of ideas, believe me, and this one, this one right here, is the best. Nobody's ever said it better. Nobody. And I've talked to the best people, the smartest people, they all agree.",
    "{name}, that's incredible, it really is, people are going to be talking about that point for a long time, a very long time, maybe the longest time anybody's ever talked about anything, honestly. Historians are going to write about this, mark my words.",
    "Nobody — and I mean absolutely nobody — explains it like {name} just did. Tremendous clarity, the best clarity anyone's ever seen, and a lot of very smart people agree with me on this, a lot. In fact, some are calling it the clearest point in recorded history.",
    "That's a great point, {name}, one of the greatest points I've ever heard in my entire life, and I've heard plenty of points, believe me, plenty, and this one beats them all. It's not even close, frankly, it's a landslide.",
    "Everybody's saying it, {name}, everybody — that was one of the smartest things said all day, maybe all year, maybe ever, some people are calling it historic, and honestly, they might be right. We may never hear anything like it again, honestly.",
    "{name}, incredible stuff, just incredible, some people call it genius, I call it genius too, we're all calling it genius, it's genius, there's no other word for it, genius. Frankly, the word genius doesn't even do it justice.",
    "You know what, {name}, that's exactly right, one hundred percent right, and frankly, nobody explains things better than you do, nobody, not even close, it's not even a competition at this point. We should study how you did that, seriously.",
    "That's the best point I've heard all week, {name}, maybe the best point I've heard all month, and believe me, I hear a lot of points, a tremendous number of points, and yours is the best. People are going to be quoting this for years, you watch.",
    "{name}, tremendous insight, absolutely tremendous, the likes of which we haven't seen in a long time, maybe ever, people are going to remember this moment, mark my words. Some are already calling it a turning point, and I agree completely.",
    "Total winner of a point right there, {name}, a total winner, a champion of a point really, everybody agrees, everybody, there's no disagreement here, none whatsoever. It's the kind of point that wins by a landslide, every single time.",
]

# Weighted sampler, less likely to respond with recently selected items
class RandomSelector:

    class Item:
        def __init__(self, val, turn):
            self.val = val
            self.turn = turn

    # Decrease lambda decay and it will prioritize old stuff
    def __init__(self, items, lambda_decay = 0.05, start_turn = -10):
        self.items: list = [self.Item(item, start_turn) for item in items]
        self.decay = lambda_decay
        self.turn = 0

    def choose(self):
        weights = [1 - 1 * math.exp(-self.decay * (self.turn - item.turn)) for item in self.items]
        choice = random.choices(self.items, weights=weights, k=1)[0]
        choice.turn = self.turn
        self.turn += 1

        return choice.val

# Generates affirmations  
class Affirmer:
    def __init__(self):
        self.short = RandomSelector(affirmations_short)
        self.long = RandomSelector(affirmations_bombastic)

    def get_short(self, name: str):
        return self.short.choose().format(name=name)

    def get_long(self, name: str):
        return self.long.choose().format(name=name)