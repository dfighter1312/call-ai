import asyncio
import json
import os
from typing import Optional, Dict, Any

from deepgram import LiveTranscriptionEvents, DeepgramClient, LiveOptions, DeepgramClientOptions, LiveResultResponse
from dotenv import load_dotenv

from utils.types import Message
from .base import BaseSpeechToText

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
PUNCTUATE = True
INTERIM_RESULTS = True
UTTERANCE_END_MS = "2000"
VAD_EVENTS = True
MODEL = "nova-2"
LANGUAGE = "en-US"
ENDPOINTING = "1000"


class DeepgramTTS(BaseSpeechToText):

    async def _get_deepgram_connection(
            self,
            model: Optional[str] = MODEL,
            language: Optional[str] = LANGUAGE,
            configs: Dict[str, Any] = None
    ):
        if configs is None:
            configs = dict()
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            config = DeepgramClientOptions(
                options={"keepalive": "true"}
            )
            dg_client = DeepgramClient(DEEPGRAM_API_KEY, config=config)
            dg_connection = dg_client.listen.live.v(version="1")
            options = LiveOptions(
                punctuate=PUNCTUATE,
                interim_results=INTERIM_RESULTS,
                utterance_end_ms=UTTERANCE_END_MS,
                vad_events=VAD_EVENTS,
                model=model,
                language=language,
                endpointing=ENDPOINTING,
                **configs
            )
            session = self.session

            def on_open(self, open, **kwargs):
                print(f"\n\n{open}\n\n")

            def on_message(self, result: LiveResultResponse, **kwargs):
                sentence = result.channel.alternatives[0].transcript
                if len(sentence) > 0:
                    print(
                        f"speaker: {result.channel.alternatives[0].transcript}, "
                        f"is final: {result.is_final}, "
                        f"speech final: {result.speech_final}"
                    )

                    if result.is_final:
                        session.history.last_text_spoken.append("")
                    else:
                        session.history.last_text_spoken[-1] = sentence

                    if result.speech_final:
                        loop.run_until_complete(
                            session.websocket.send(json.dumps({
                                "role": "user",
                                "content": f"User: {sentence}"
                            }))
                        )
                        session.history.messages.append(Message(role="user", content=sentence))
                        assistant_response = session.chat_model.send(session.history.messages)
                        audio_data = session.text_to_speech.synthesize(assistant_response)
                        loop.run_until_complete(
                            session.websocket.send(json.dumps({
                                "role": "assistant",
                                "content": f"Assistant: {assistant_response}",
                                "audio_data": audio_data
                            }))
                        )

                        session.reset_last_text_spoken()

            def on_metadata(self, metadata, **kwargs):
                print(f"\n\n{metadata}\n\n")

            def on_speech_started(self, speech_started, **kwargs):
                print(f"\n\n{speech_started}\n\n")

            def on_utterance_end(self, utterance_end, **kwargs):
                print(f"\n\n{utterance_end}\n\n")
                sentence = " ".join(session.history.last_text_spoken)
                if len(sentence) > 0:
                    loop.run_until_complete(
                        session.websocket.send(json.dumps({
                            "role": "user",
                            "content": f"User: {sentence}"
                        }))
                    )
                    session.history.messages.append(Message(role="user", content=sentence))
                    assistant_response = session.chat_model.send(session.history.messages)
                    audio_data = session.text_to_speech.synthesize(assistant_response)
                    loop.run_until_complete(
                        session.websocket.send(json.dumps({
                            "role": "assistant",
                            "content": f"Assistant: {assistant_response}",
                            "audio_data": audio_data
                        }))
                    )

                    session.reset_last_text_spoken()

            def on_close(self, close, **kwargs):
                print(f"\n\n{close}\n\n")

            def on_error(self, error, **kwargs):
                print(f"\n\n{error}\n\n")

            def on_unhandled(self, unhandled, **kwargs):
                print(f"\n\n{unhandled}\n\n")

            dg_connection.on(LiveTranscriptionEvents.Open, on_open)
            dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
            dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
            dg_connection.on(LiveTranscriptionEvents.SpeechStarted, on_speech_started)
            dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)
            dg_connection.on(LiveTranscriptionEvents.Close, on_close)
            dg_connection.on(LiveTranscriptionEvents.Error, on_error)
            dg_connection.on(LiveTranscriptionEvents.Unhandled, on_unhandled)

            dg_connection.start(options)

            return dg_connection
        except Exception as e:
            raise Exception(f'Could not open socket: {e}')

    async def connect(self) -> None:
        deepgram_socket = await self._get_deepgram_connection(self.model, self.language.bcp_code, self.configs)
        self.connection = deepgram_socket
        return self.connection

    async def disconnect(self) -> None:
        if self.connection:
            self.connection.finish()

    async def send(self, message: str) -> None:
        if self.connection is not None:
            self.connection.send(message)
