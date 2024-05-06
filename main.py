import asyncio
import logging
import uuid
from typing import Dict

import websockets
from websockets import WebSocketServerProtocol

from llm import LLM
from session.manage import Session
from speech_to_text import SpeechToText
from text_to_speech.factory import TextToSpeech
from utils.parser import parse_path
from utils.types.history import VideoCallSessionHistory
from utils.types.language import Language

connected_clients: Dict[str, Session] = {}
connected_tts_models: Dict[str, SpeechToText] = {}


async def handle_connection(websocket: WebSocketServerProtocol, path: str):

    request = parse_path(path)
    client_id = str(uuid.uuid4())

    # TODO: Collect more information from User ID and Scenario ID, with the corresponding chat models
    language = Language("English")
    connected_clients[client_id] = Session(
        websocket=websocket,
        history=VideoCallSessionHistory(messages=[], last_text_spoken=[""]),
        chat_model=LLM("gpt-3.5"),
        text_to_speech=TextToSpeech("google", voice="en-US-Wavenet-A", language=language)
    )
    try:
        if request.path == "/listen":
            connected_tts_models[client_id] = SpeechToText("google")

            # Retrieve the session and text to speech instance again from the list
            session = connected_clients[client_id]
            speech_to_text = connected_tts_models[client_id]

            # Begin the speech to text listener
            await speech_to_text.start(session=session)

            # For every chunk sent from the FE, it will be sent to the Speech to text to handle the audio data
            # STT API will also handle the logic of sending LLM request and convert the LLM response
            # into audio then send back to the FE
            async for message in websocket:
                await speech_to_text.send(message)

        else:
            raise ValueError("Invalid path")

    except websockets.exceptions.ConnectionClosed as e:
        logging.exception(e, exc_info=True)

    except Exception as e:
        logging.exception(e, exc_info=True)

    # Triggered when connection is closed or there is any exception occurred
    finally:
        logging.info("Closing websocket connection")
        connected_clients.pop(client_id, None)
        tts_model = connected_tts_models.pop(client_id, None)
        if tts_model is not None:
            await tts_model.stop()


if __name__ == "__main__":
    start_server = websockets.serve(handle_connection, "localhost", 5555)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
