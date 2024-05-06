from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from session.manage import Session
from utils.types.language import Language


class BaseSpeechToText(ABC):

    def __init__(
            self,
            session: Session,
            model: Optional[str] = None,
            language: Optional[Language] = None,
            configs: Dict[str, Any] = None
    ):
        self._session = session
        self._model = model
        self._language = language
        self._configs = configs
        self._connection = None

    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        pass

    @abstractmethod
    async def send(self, message: str) -> None:
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

    @property
    def model(self):
        return self._model

    @property
    def language(self):
        return self._language

    @property
    def configs(self):
        return self._configs
