# you-re-absolutely-right

You're absolutely right is a life changing discord bot that affirms your brilliant ideas. It has 2 modes, text and voice. You can trigger it via text by reacting with a 100% emoji and it will send out the positive affirmation your friends were going to soon send you.

<img width="600" height="272" alt="image-3" src="https://github.com/user-attachments/assets/d66e208e-2a81-4171-868e-0bdaface7962" />

Ping @You're Absolutely Right and it will back you up with praise in your vc. There hasn't been any issues with memory usage (yet).

https://github.com/user-attachments/assets/c657b75c-46d7-4d33-af7b-6607960b0aa4


Install into your discord server with this [link](https://discord.com/oauth2/authorize?client_id=1531312045511933954)

## Features

- **Reaction-Triggered Text**: React with 💯 to get a text affirmation.
- **Ping-Triggered Voice**: While in a VC, ping the bot to hear it back you up.
- **Configurable TTS Engines**:
    - **ElevenLabs**: High-quality, realistic speech (requires API key).
    - **Piper (Local)**: Lightweight, local TTS that runs on < 1 GB RAM.
- **Name Processing**: Uses `wordninja` to split concatenated usernames (e.g., "coolguy123" -> "cool guy 123") for natural pronunciation.
- **Audio Caching**: Lazily generates and caches audio fragments to minimize API calls and improve response time.
- **Spam Protection**: Built-in rate limiting (4 affirmation messages per 50 seconds per user) to prevent spam.
- **Privacy**: No message history is logged. Only saved data is usernames which is used for caching.

The bot is hosted on oracle cloud so you can simply add the bot to your own server without needing to interact with any of this source code using this installation link. To guard against mass reactions to spam, the bot's reply messages are rate limited to 4 per 50s per user. There hasn't been any issues with RAM (yet).

The TTS is very configurable, it currently uses ElevenLabs for a realistic TTS. There is a decent local TTS option but the speech is less realistic and you will need to set it up yourself. Works well with the ElevenLabs free plan due to the caching used, generally only thing that needs TTS is username on a user's first use, then it works by just concatenating together wav files.

You can also setup this bot fairly simply, pip install requirements, make a bot using the discord developer bot then copy its details into a .env. Eleven labs options can be left empty if you are using the local piper TTS. The TTS is very configurable if you want to swap it out also.

```py
# Just make a TTS that conforms to AbstractTTS, then in main have Affirmer use it.
# Then you're done, caching and etc is all separated from the model used 
guild_affirmers: defaultdict[Guild, Affirmer] = defaultdict(lambda: Affirmer(ElevenLabsTTS()))
```

.env
```
APP_ID=...
PUBLIC_KEY=...
TOKEN=...
ELEVEN_LABS_API=...
ELEVEN_LABS_VOICE_ID=...
```

Now run main.py and you're good to go.
