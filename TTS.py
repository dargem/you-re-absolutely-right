from abc import ABC, abstractmethod
from pathlib import Path
from piper import PiperVoice, SynthesisConfig

class AbstractTTS(ABC):
    @abstractmethod
    def generate_text(text: str, path: Path):
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

    def generate_text(text: str, path: Path):
        with 
    