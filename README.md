# Real-Time AI Conversation System

This repository contains the implementation of a real-time AI conversation system. It utilizes a speech-to-text model to convert user speech into text, processes the text through a large language model (LLM) to generate responses, and finally uses a text-to-speech model to convert the responses back into speech.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

```bash
pip install -r requirements.txt
```

You should also ask the author to get the .env file and Google service account file (JSON format), or get it on your own.
```env
DEEPGRAM_API_KEY=<YOUR_DEEPGRAM_API_KEY>
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
GROQ_API_KEY=<YOUR_GROQ_API_KEY>
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

Follow the on-screen instructions to interact with the AI. Make sure your microphone is enabled as the system listens to your input in real-time.

## Architecture

This system is composed of three main components:

1. **Speech-to-Text Model:** Converts user speech into text. This repository uses Deepgram.
2. **Large Language Model (LLM):** Processes the text to generate intelligent responses. This implementation utilizes GPT-3.5 Turbo.
3. **Text-to-Speech Model:** Converts the text responses back into speech, allowing for a spoken conversation with the AI. Google TTS is used here.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Darwin Nguyen (Hoang-Dung Nguyen)** - *Initial work* - [dfighter1312](https://github.com/dfighter1312)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc.
