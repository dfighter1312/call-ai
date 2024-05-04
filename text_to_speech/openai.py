from text_to_speech.base import BaseTextToSpeech


class OpenAITextToSpeech(BaseTextToSpeech):
    def synthesize(self, text: str, voice: str = 'en-US', language: str = 'en-US') -> str:
        pass