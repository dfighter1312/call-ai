import asyncio
import json
import logging
import queue
import os
import queue
import threading
from typing import Optional, Dict, Any, Iterable

import google.api_core.exceptions
from google.cloud.speech import SpeechClient, RecognitionConfig, StreamingRecognitionConfig, StreamingRecognizeRequest, \
    StreamingRecognizeResponse

from session.manage import Session
from speech_to_text.base import BaseSpeechToText
from utils.tags.classes import experimental
from utils.types import Message
from utils.types.language import Language

GOOGLE_ACCOUNT_CREDENTIALS = os.getenv('GOOGLE_ACCOUNT_CREDENTIALS')


@experimental
class GoogleTTS(BaseSpeechToText):
    """Implementation is based on
    https://github.com/dawntcherian/Google-speech-to-text-python-websocket-server-using-microphone-stream/blob/master/websocket_server.py
    and https://cloud.google.com/speech-to-text/docs/transcribe-streaming-audio#endless-streaming"""

    def __init__(
            self,
            session: Session,
            model: Optional[str] = None,
            language: Optional[Language] = Language("English"),
            configs: Dict[str, Any] = None
    ):
        super().__init__(session, model, language, configs)
        self.buff = queue.Queue()
        self.closed = True
        self.transcript = None
        self.thread = None

    def _handle_responses(self, responses: Iterable[StreamingRecognizeResponse]):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        print("Start generating transcripts")
        for response in responses:
            for result in response.results:
                alternatives = result.alternatives
                # The alternatives are ordered from most likely to least.
                # transcript = alternatives[0].transcript
                for alternative in alternatives:
                    sentence = alternative.transcript
                    loop.run_until_complete(self.session.websocket.send(json.dumps({
                        "role": "user",
                        "content": f"User: {sentence}"
                    })))
                    self.session.history.messages.append(Message(role="user", content=sentence))
                    assistant_response = self.session.chat_model.send(self.session.history.messages)
                    audio_data = self.session.text_to_speech.synthesize(assistant_response)
                    loop.run_until_complete(
                        self.session.websocket.send(json.dumps({
                            "role": "assistant",
                            "content": f"Assistant: {assistant_response}",
                            "audio_data": audio_data
                        }))
                    )

                    self.session.reset_last_text_spoken()

        # for response in responses:
        #     print("Received response: {}".format(response))
        #     print("Received text: {}".format(response.results[0].alternatives[0].transcript))
        #     if not response.results:
        #         continue
        #     result = response.results[0]
        #
        #     if not result.alternatives:
        #         continue
        #     transcript = result.alternatives[0].transcript
        #     if result.is_final:
        #         self.transcript = transcript
        # if self.transcript:
        #     print(self.transcript)

    def _process(self):
        """Audio stream recognition and result parsing"""
        client = SpeechClient.from_service_account_json(filename=GOOGLE_ACCOUNT_CREDENTIALS)
        config = RecognitionConfig(
            encoding=RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=32000,
            language_code=self.language.bcp_code
        )
        streaming_config = StreamingRecognitionConfig(
            config=config,
            interim_results=False,
            single_utterance=False
        )
        audio_generator = self._stream_generator()
        requests = (StreamingRecognizeRequest(audio_content=content) for content in audio_generator)
        responses = client.streaming_recognize(requests=requests, config=streaming_config)
        try:
            self._handle_responses(responses)
        except google.api_core.exceptions.OutOfRange:
            logging.error("Stream is out of range")
            threading.Thread(target=self._process).start()
            pass

    def _stream_generator(self):
        while not self.closed:
            chunk = self.buff.get()
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = self.buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b''.join(data)

    async def connect(self) -> None:
        threading.Thread(target=self._process).start()
        pass

    async def disconnect(self) -> None:
        self.closed = True

    async def send(self, message: str) -> None:
        self.buff.put(message)
        self.closed = False
