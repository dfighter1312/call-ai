from enum import Enum


class SpeechToTextProvider(str, Enum):
    DEEPGRAM = "deepgram"
    GOOGLE = "google"
