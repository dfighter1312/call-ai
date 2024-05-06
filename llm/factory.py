from typing import Union, Dict, List

from utils.types import Message
from .base import BaseLLM
from .openai import OpenAIModel
from utils.enums import LLMModel


class LLM:
    models: Dict[LLMModel, BaseLLM] = {
        LLMModel.GPT_3_5: OpenAIModel("gpt-3.5"),
        LLMModel.GPT_4: OpenAIModel("gpt-4"),
    }

    def __init__(self, model_name: Union[str, LLMModel]):
        if isinstance(model_name, str):
            model_name = LLMModel(model_name)

        self._model = self.models.get(model_name)

    def send(self, messages: List[Message]):
        messages = self._model.format_messages(messages)
        response = self._model.get_chat_response(messages)
        return response.response.content
