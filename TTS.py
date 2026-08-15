from abc import ABC, abstractmethod
from pathlib import Path
from piper import PiperVoice, SynthesisConfig
import wave
from elevenlabs import save
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
import os

class AbstractTTS(ABC):
    @abstractmethod
    def generate_text(self, text: str, path: Path):
        pass

    # Get identifier for model name so we know what we are "dealing with" for caching
    # In practice can just be the name of the model + config options
    @abstractmethod
    def get_model_id(self) -> str:
        pass


class PiedPierTTS(AbstractTTS):
    def __init__(
        self, 
        syn_config: SynthesisConfig = SynthesisConfig(
            length_scale=0.9, # increase to make it slower
            noise_w_scale=1,  # increase to make more speaking variation
            normalize_audio=False, # use raw audio from voice
        ),
        voice: PiperVoice = PiperVoice.load("en_US-lessac-medium.onnx")
    ):
        self.config = syn_config
        self.voice = voice

    def generate_text(self, text: str, path: Path):
        with wave.open(str(path), "wb") as wav_f:
            self.voice.synthesize_wav(
                text,
                wav_f,
                syn_config=self.config
            )

    

load_dotenv()

class ElevenLabsTTS(AbstractTTS):
    def __init__(
        self, client: ElevenLabs = ElevenLabs(api_key=os.getenv("ELEVEN_LABS_API"))
    ):
        self.client = client

    def generate_text(self, text: str, path: Path):
        audio = self.client.generate(
            text=text,
            voice="Rachel",
            model="eleven_multilingual_v2"
        )

        save(audio, str(path))
        
