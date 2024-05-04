from typing import List

from pydantic import BaseModel

from .message import Message


class VideoCallSessionHistory(BaseModel):

    messages: List[Message]

    last_text_spoken: List[str]