from abc import ABC, abstractmethod
from typing import List

from utils.types import Message, LLMChatRequest
from utils.types.llm_response import LLMChatResponse


class BaseLLM(ABC):

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
    