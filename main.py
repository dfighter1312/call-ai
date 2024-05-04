import asyncio
import uuid
from typing import Dict
from urllib.parse import urlparse, parse_qs

import websockets
from websockets import WebSocketServerProtocol

from llm import LLM
from session.manage import Session
from speech_to_text import SpeechToText
from text_to_speech.factory import TextToSpeech
from utils.types.history import VideoCallSessionHistory

connected_clients: Dict[str, Session] = {}
connected_tts_models: Dict[str, SpeechToText] = {}


async def handle_connection(websocket: WebSocketServerProtocol, path: str):
    # Parse the URL to extract query parameters
    url = urlparse(path)
    query_params = parse_qs(url.query)

    # Extract user_id and scenario_id from the query parameters
    user_id = query_params.get('user_id', [None])[0]
    scenario_id = query_params.get('scenario_id', [None])[0]
    language = query_params.get('language', ['en-US'])[0]  # Defaulting to 'en-US' if not specified
    print("Query parameters:", user_id, scenario_id, language)

    client_id = str(uuid.uuid4())

    # TODO: Collect more information from User ID and Scenario ID
    connected_clients[client_id] = Session(
        websocket=websocket,
        history=VideoCallSessionHistory(messages=[], last_text_spoken=[""]),
        chat_model=LLM("gpt-3.5"),
        text_to_speech=TextToSpeech("google", voice="en-US-Wavenet-A", language="en-US")
    )
    try:
        if url.path == "/listen":
            connected_tts_models[client_id] = SpeechToText("deepgram")

            session = connected_clients[client_id]
            text_to_speech = connected_tts_models[client_id]

            await text_to_speech.start(session=session)
            async for message in websocket:
                await text_to_speech.send(message)

        else:
            raise ValueError("Invalid path")

    finally:
        connected_clients.pop(client_id, None)
        tts_model = connected_tts_models.pop(client_id, None)
        if tts_model is not None:
            await tts_model.stop()


if __name__ == "__main__":
    start_server = websockets.serve(handle_connection, "localhost", 5555)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
