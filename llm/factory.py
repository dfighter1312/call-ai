from typing import Union, Dict, List

from utils.types import Message
from .base import BaseLLM
from .groq import GroqModel
from .openai import OpenAIModel
from utils.enums import LLMModel


class LLM:
    models: Dict[LLMModel, BaseLLM] = {
        LLMModel.GPT_3_5: OpenAIModel("gpt-3.5"),
        LLMModel.GPT_4: OpenAIModel("gpt-4"),
        
        # Experimental classes
        LLMModel.LLAMA_2_70B: GroqModel("llama2-70b-4096"),
        LLMModel.MIXTRAL_8X7B: GroqModel("mixtral-8x7b-32768"),
        LLMModel.GEMMA_7B: GroqModel("gemma-7b-it")
    }

    def __init__(self, model_name: Union[str, LLMModel]):
        if isinstance(model_name, str):
            model_name = LLMModel(model_name)

        self._model = self.models.get(model_name)

    def send(self, messages: List[Message]):
        messages = self._model.format_messages(messages)
        response = self._model.get_chat_response(messages)
        return response.response.content
