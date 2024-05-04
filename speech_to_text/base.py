from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from session.manage import Session


class BaseSpeechToText(ABC):

    def __init__(
            self,
            session: Session,
            model: Optional[str] = None,
            language: Optional[str] = None,
            configs: Dict[str, Any] = None
    ):
        self._session = session
        self._model = model
        self._language = language
        self._configs = configs
        self._connection = None

    @abstractmethod
    async def _connect(
            self,
            model: Optional[str] = None,
            language: Optional[str] = None,
            configs: Dict[str, Any] = None
    ) -> None:
        pass

    @abstractmethod
    async def _disconnect(self) -> None:
        pass

    @abstractmethod
    async def _send(self, message: str) -> None:
        pass

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session):
        self._session = session

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, connection):
        self._connection = connection

    async def connect(self):
        return await self._connect(self._model, self._language, self._configs)

    async def disconnect(self):
        await self._disconnect()

    async def send(self, message: str) -> None:
        if self.connection:
            await self._send(message)
