from typing import Optional

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

from utils.tags.classes import experimental
from utils.types.language import Language
from .base import BaseTextToSpeech


load_dotenv()


@experimental
class ElevenLabsTextToSpeech(BaseTextToSpeech):

    def synthesize(self, text: str, voice: Optional[str] = None, language: Language = Language("English")) -> str:
        client = ElevenLabs()
        if voice is None:
            voice = client.voices.get_all()[0]
        audio = client.generate(
            text=text,
            voice=voice,
            model="eleven_multilingual_v2"
        )
        return bytes(*audio).decode()
