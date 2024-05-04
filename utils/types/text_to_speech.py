from enum import Enum


class TextToSpeechProvider(str, Enum):
    GOOGLE = "google"
    OPENAI = "openai"
    ELEVENLABS = "elevenlabs"
