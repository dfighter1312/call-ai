from abc import ABC, abstractmethod
from typing import Optional

from utils.types.language import Language


class BaseTextToSpeech(ABC):

    @abstractmethod
    def synthesize(self, text: str, voice: Optional[str] = None, language: Language = Language("English")) -> str:
        pass
