from enum import Enum


class LLMModel(str, Enum):
    GPT_3_5 = "gpt-3.5"
    GPT_4 = "gpt-4"
