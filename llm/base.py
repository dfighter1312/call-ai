from abc import ABC, abstractmethod
from typing import List, Optional

from utils.types import Message, LLMChatRequest
from utils.types.llm_response import LLMChatResponse


class BaseLLM(ABC):

    @abstractmethod
    def __init__(self, model: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def format_messages(self, message_history: List[Message]) -> LLMChatRequest:
        """
        Formats the input messages according to the requirements of the model.
        Implementation template example:


        Args:
            message_history (MessageHistory): List of messages, where each message
                        is a dictionary with 'role' and 'content' keys.

        Returns:
            Formatted message
        """
        raise NotImplementedError

    @abstractmethod
    def get_chat_response(self, request: LLMChatRequest) -> LLMChatResponse:
        """
        Get the response from the model
        
        Args:
            request (LLMChatRequest): Message request
            
        Returns:
            LLMChatResponse: Response from the model
        """
        raise NotImplementedError

    def set_models(self, chat_model: Optional[str], completion_model: Optional[str]) -> None:
        self._chat_model = chat_model
        self._completion_model = completion_model

    @property
    def chat_model(self) -> str:
        return self._chat_model

    @property
    def completion_model(self):
        return self._completion_model
