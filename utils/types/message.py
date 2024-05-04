from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ChatRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    """Message object"""

    role: ChatRole
    """Role of the user who sent the message"""

    content: Optional[str] = None
    """Content of the message"""
