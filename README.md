# Multi-Agent Thinking Chat 🤖

A modular Streamlit application that provides a unified interface for interacting with multiple AI agents, featuring a unique thinking process visualization for supported models.

## Features

- Support for multiple AI agents:
  - OpenAI Agent (GPT-4 Turbo)
  - Anthropic Agent (Claude 3 Opus)
  - Google Agent (Gemini Pro with thinking process)
  - Together AI Agent (Mixtral-8x7B)
  - OpenRouter Agent (Multiple Models Hub)
- Real-time streaming responses
- Unique thinking process visualization (Gemini Pro only)
- Clean, modular architecture for easy extension
- Secure environment-based API key management
- Persistent chat history with thinking process support

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package and dependencies:
```bash
pip install -e .
```

## Configuration

1. Get API keys from the providers you want to use:
   - OpenAI: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Anthropic: Get from [Anthropic Console](https://console.anthropic.com/)
   - Google: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Together AI: Get from [Together AI Platform](https://www.together.ai/api)
   - OpenRouter: Get from [OpenRouter Dashboard](https://openrouter.ai/keys)

2. Create a .env file in the project root:
```bash
cp .env.example .env
```

3. Add your API keys to the .env file:
```env
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
GOOGLE_API_KEY=your-google-api-key
TOGETHER_API_KEY=your-together-api-key
OPENROUTER_API_KEY=your-openrouter-api-key
```

Note: You only need to add API keys for the agents you want to use. The application will automatically detect available agents based on the API keys present in your .env file.

## Usage

1. Start the Streamlit application:
```bash
streamlit run src/main.py
```

2. Select an agent from the selection panel
3. Click "Initialize Agent" to start chatting

## Project Structure

```
src/
├── agents/           # Agent implementations
│   ├── base.py      # Base agent interface
│   ├── openai.py    # OpenAI agent
│   ├── anthropic.py # Anthropic agent
│   ├── gemini.py    # Google Gemini agent
│   ├── together.py  # Together AI agent
│   └── openrouter.py # OpenRouter agent
├── ui/              # Streamlit interface components
│   ├── app.py       # Main application
│   ├── components.py # UI components
│   └── config.py    # Configuration and settings
├── utils/           # Utility functions
│   └── config.py    # Environment configuration
└── main.py          # Entry point
```

## Extending

To add support for a new AI agent:

1. Create a new agent class in `src/agents/` that inherits from `BaseAgent`
2. Implement the required methods:
   - `_initialize()`
   - `stream_chat()`
   - `model_name` property
3. Add the agent configuration to `AVAILABLE_MODELS` in `src/ui/config.py`
4. Add the API key name to `.env.example`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License
