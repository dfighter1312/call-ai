from typing import List, Literal

from dotenv import load_dotenv
from groq import Groq

from llm.base import BaseLLM
from utils.tags.classes import experimental
from utils.types import Message, GroqChatRequest
from utils.types.llm_response import GroqChatResponse

load_dotenv()


@experimental
class GroqModel(BaseLLM):

    def __init__(self, model: str):
        if model not in ["llama2-70b-4096", "mixtral-8x7b-32768", "gemma-7b-it"]:
            raise ValueError(f"Invalid model name: {model}")
        self.set_models(model, model)

    def format_messages(self, message_history: List[Message]) -> GroqChatRequest:
        return GroqChatRequest(messages=[m.model_dump() for m in message_history])

    def get_chat_response(self, request: GroqChatRequest) -> GroqChatResponse:
        client = Groq()
        response = client.chat.completions.create(
            model=self.chat_model,
            messages=request.model_dump()["messages"]
        )
        return GroqChatResponse(
            response=response.choices[0].message.model_dump()
        )
