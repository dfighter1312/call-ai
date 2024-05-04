from typing import List, Literal

from dotenv import load_dotenv
from openai import OpenAI

from llm.base import BaseLLM
from utils.types import Message, OpenAIChatRequest
from utils.types.llm_response import OpenAIChatResponse


load_dotenv()


class OpenAIModel(BaseLLM):

    def __init__(self, model: Literal["gpt-3.5", "gpt-4"]):
        if model == "gpt-3.5":
            self.chat_model = "gpt-3.5-turbo"
            self.completion_model = "gpt-3.5-turbo-instruct"
        elif model == "gpt-4":
            self.chat_model = "gpt-4-1106-preview"
            self.completion_model = "gpt-4-1106-preview"
        self.vision_model = "gpt-4-vision-preview"

        self.client = OpenAI()

    def format_messages(self, message_history: List[Message]) -> OpenAIChatRequest:
        return OpenAIChatRequest(messages=[m.model_dump() for m in message_history])

    def get_chat_response(self, request: OpenAIChatRequest) -> OpenAIChatResponse:
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=request.model_dump()["messages"]
        )
        return OpenAIChatResponse(
            response=response.choices[0].message.model_dump()
        )
