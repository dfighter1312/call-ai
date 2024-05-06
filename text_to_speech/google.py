import base64
import os

import google.cloud.texttospeech as tts
from dotenv import load_dotenv

from utils.types.language import Language
from .base import BaseTextToSpeech

load_dotenv()

GOOGLE_ACCOUNT_CREDENTIALS = os.getenv('GOOGLE_ACCOUNT_CREDENTIALS')
client = tts.TextToSpeechClient.from_service_account_json(GOOGLE_ACCOUNT_CREDENTIALS)


class GoogleTextToSpeech(BaseTextToSpeech):

    def synthesize(self, text: str, voice: str = 'en-US', language: Language = Language("English")) -> str:
        text_input = tts.SynthesisInput(text=text)
        voice_params = tts.VoiceSelectionParams(
            language_code=language.bcp_code, name=voice
        )
        audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

        response = client.synthesize_speech(
            input=text_input,
            voice=voice_params,
            audio_config=audio_config,
        )
        return base64.b64encode(response.audio_content).decode()
