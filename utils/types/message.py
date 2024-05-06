from typing import Optional

from pydantic import BaseModel

from utils.enums.role import ChatRole


class Message(BaseModel):
    """Message object"""

    role: ChatRole
    """Role of the user who sent the message"""

    content: Optional[str] = None
    """Content of the message"""
