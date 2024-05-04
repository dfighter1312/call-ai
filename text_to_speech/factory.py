from typing import Union, Optional

from utils.types.text_to_speech import TextToSpeechProvider
from .elevenlabs import ElevenLabsTextToSpeech
from .google import GoogleTextToSpeech
from .openai import OpenAITextToSpeech


class TextToSpeech:
    models = {
        TextToSpeechProvider.OPENAI: OpenAITextToSpeech(),
        TextToSpeechProvider.GOOGLE: GoogleTextToSpeech(),
        TextToSpeechProvider.ELEVENLABS: ElevenLabsTextToSpeech()
    }

    def __init__(
            self,
            provider: Union[str, TextToSpeechProvider],
            voice: Optional[str] = None,
            language: Optional[str] = None
    ):
        if isinstance(provider, str):
            provider = TextToSpeechProvider(provider)
        self._model = self.models.get(provider, None)
        if not self._model:
            raise ValueError(f"Invalid provider: {provider}")

        self._voice = voice
        self._language = language

    def synthesize(self, text: str) -> str:
        return self._model.synthesize(text, self._voice, self._language)
