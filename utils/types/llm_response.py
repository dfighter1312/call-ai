from typing import Optional

from pydantic import BaseModel

from utils.types import Message


class LLMChatResponse(BaseModel):
    """Represents a response from the LLM"""
    response: Message

    input_token_usage: Optional[int] = None

    output_token_usage: Optional[int] = None

    total_token_usage: Optional[int] = None

    # You can add more fields for later logging #


class OpenAIChatResponse(LLMChatResponse):
    """Represents a response from the OpenAI API"""
    pass


class GroqChatResponse(LLMChatResponse):
    """Represents a response from the Groq API"""
    pass
