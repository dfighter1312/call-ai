from abc import ABC, abstractmethod


class BaseTextToSpeech(ABC):

    @abstractmethod
    def synthesize(self, text: str, voice: str = 'en-US', language: str = 'en-US') -> str:
        pass
