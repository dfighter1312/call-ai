from utils.tags.classes import experimental
from utils.types.language import Language
from .base import BaseTextToSpeech


@experimental
class ElevenLabsTextToSpeech(BaseTextToSpeech):
    def synthesize(self, text: str, voice: str = 'en-US', language: Language = Language("English")) -> str:
        pass