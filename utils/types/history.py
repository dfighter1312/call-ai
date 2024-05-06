from typing import List

from pydantic import BaseModel

from .message import Message


class VideoCallSessionHistory(BaseModel):

    messages: List[Message]
    """List of messages sent by the user and AI agent."""

    last_text_spoken: List[str]
    """Last detected sentence spoken by the user. This is useful when the speech to text provider decided
    to reset the sentence output to record the new sentence (when is_final is True, in Deepgram, for example)."""
