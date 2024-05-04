from typing import List, Dict, Any

from pydantic import BaseModel

from .message import Message


class LLMChatRequest(BaseModel):
    messages: List[Message]
    """List of messages to send to the model."""

    include_images: bool = False
    """Whether to use the vision model in inference mode."""

    configs: Dict[str, str] = {}
    """Configurations to pass to the model"""


class OpenAIChatRequest(LLMChatRequest):
    pass


class GroqChatRequest(LLMChatRequest):
    pass
