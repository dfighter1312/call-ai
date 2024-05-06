from enum import Enum


class LLMModel(str, Enum):
    GPT_3_5 = "gpt-3.5"
    GPT_4 = "gpt-4"
    LLAMA_2_70B = "llama2-70b-4096"
    MIXTRAL_8X7B = "mixtral-8x7b-32768"
    GEMMA_7B = "gemma-7b-it"
