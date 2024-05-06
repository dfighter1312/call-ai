from websockets import WebSocketServerProtocol

from llm import LLM
from text_to_speech.factory import TextToSpeech
from utils.types import VideoCallSessionHistory


class Session:
    """Containing session data"""

    websocket: WebSocketServerProtocol
    """WebSocket server"""

    history: VideoCallSessionHistory
    """Video call session chat history"""

    chat_model: LLM
    """LLM model instance"""

    text_to_speech: TextToSpeech
    """Text to speech instance"""

    def __init__(
            self,
            websocket: WebSocketServerProtocol,
            history: VideoCallSessionHistory,
            chat_model: LLM,
            text_to_speech: TextToSpeech,
    ):
        self.websocket = websocket
        self.history = history
        self.chat_model = chat_model
        self.text_to_speech = text_to_speech

    def reset_last_text_spoken(self):
        self.history.last_text_spoken = [""]
