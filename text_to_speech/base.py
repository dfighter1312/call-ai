from abc import ABC, abstractmethod

from utils.types.language import Language


class BaseTextToSpeech(ABC):

    @abstractmethod
    def synthesize(self, text: str, voice: str = 'en-US', language: Language = Language("English")) -> str:
        pass
