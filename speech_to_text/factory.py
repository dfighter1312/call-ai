from typing import Any, Optional, Dict, Union

from session.manage import Session
from utils.enums import SpeechToTextProvider
from utils.types.language import Language
from .base import BaseSpeechToText
from .deepgram import DeepgramTTS
from .google import GoogleTTS


class SpeechToText:
    models: dict[SpeechToTextProvider, type[BaseSpeechToText]] = {
        SpeechToTextProvider.DEEPGRAM: DeepgramTTS,

        # Experimental classes
        SpeechToTextProvider.GOOGLE: GoogleTTS,
    }

    def __init__(
            self,
            provider: Union[str, SpeechToTextProvider],
            model: Optional[str] = None,
            language: Optional[Language] = Language("English"),
            configs: Dict[str, Any] = None
    ) -> None:
        if isinstance(provider, str):
            provider = SpeechToTextProvider(provider)

        self._model_instance = None
        self._model_cls = self.models.get(provider)
        if self._model_cls is None:
            raise ValueError(f"Invalid TextToSpeech provider: {provider}")
        self._language = language
        self._config = configs
        self._model = model

    async def start(self, session: Session) -> BaseSpeechToText:
        self._model_instance = self._model_cls(session, self._model, self._language, self._config)
        await self._model_instance.connect()
        return self._model_instance

    async def send(self, data: str) -> None:
        await self._model_instance.send(data)

    async def stop(self) -> None:
        await self._model_instance.disconnect()
