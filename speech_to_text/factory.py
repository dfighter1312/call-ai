from typing import Any, Optional, Dict, Union

from .deepgram import DeepgramTTS
from .google import GoogleTTS

from utils.types import SpeechToTextProvider
from session.manage import Session
from .base import BaseSpeechToText


class SpeechToText:
    models: dict[SpeechToTextProvider, type[BaseSpeechToText]] = {
        SpeechToTextProvider.DEEPGRAM: DeepgramTTS,
        SpeechToTextProvider.GOOGLE: GoogleTTS,
    }

    def __init__(
            self,
            provider: Union[str, SpeechToTextProvider],
            model: Optional[str] = None,
            language: Optional[str] = None,
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
        self._model_instance = self._model_cls(session, self._language, self._config)
        await self._model_instance.connect()
        return self._model_instance

    async def send(self, data: str) -> None:
        await self._model_instance.send(data)

    async def stop(self) -> None:
        await self._model_instance.disconnect()
