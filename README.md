# Real-Time AI Conversation System

This repository contains the implementation of a real-time AI conversation system. It utilizes a speech-to-text model to convert user speech into text, processes the text through a large language model (LLM) to generate responses, and finally uses a text-to-speech model to convert the responses back into speech.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

```bash
pip install -r requirements.txt
```

Form your `.env` file by getting API keys from the third-party providers, depending on which provider you want to use on each component.
```env
DEEPGRAM_API_KEY=<YOUR_DEEPGRAM_API_KEY>
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
GROQ_API_KEY=<YOUR_GROQ_API_KEY>
ELEVENLABS_API_KEY=<YOUR_ELEVENLABS_API_KEY>
GOOGLE_ACCOUNT_CREDENTIALS=gg_service_account.json
```

### Installing

A step-by-step series of examples that tell you how to get a development environment running:

1. Clone the repository:
   ```bash
   git clone https://github.com/dfighter1312/real-time-ai-conversation.git
   ```
2. Navigate to the cloned repository:
   ```bash
   cd real-time-ai-conversation
   ```
3. Install the necessary packages:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

To start the system, run the following command:

```bash
python main.py
```

Then, open the `index.html` file under the `html` folder to start the conversation. 
Make sure your microphone is enabled with sufficient permissions as the system listens to your input in real-time.

## Architecture

This system is composed of three main components:

1. **Speech-to-Text Model:** Converts user speech into text
- [x] Deepgram
- [x] Google STT
- [ ] OpenAI Whisper
2. **Large Language Model (LLM):** Processes the text to generate intelligent responses. 
- [x] OpenAI
- [x] Groq
- [ ] Hugging Face LLMs
3. **Text-to-Speech Model:** Converts the text responses back into speech, allowing for a spoken conversation with the AI.
- [x] Google TTS
- [x] ElevenLabs

## Planning updates

- Updating multiple languages chat
- Adding prompt for every session
- RAG integration

## Contributing

Contributions are unavailable at this time. If you are willing for any contributions, please contact me at [dfighter1312](https://github.com/dfighter1312).

## Authors

* **Darwin Nguyen (Hoang-Dung Nguyen)** - *Initial work* - [dfighter1312](https://github.com/dfighter1312)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
