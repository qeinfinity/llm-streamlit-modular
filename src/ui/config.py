from typing import Dict, List, Optional
from dataclasses import dataclass
import streamlit as st
from src.utils.config import get_api_key, load_env_config
from src.agents.base import BaseAgent
from src.agents.openai import OpenAIAgent
from src.agents.anthropic import AnthropicAgent
from src.agents.gemini import GeminiAgent
from src.agents.together import TogetherAgent
from src.agents.openrouter import OpenRouterAgent

@dataclass
class ModelConfig:
    name: str
    provider: str
    api_key_name: str
    description: str
    agent_class: type[BaseAgent]
    supports_thinking: bool = False

AVAILABLE_MODELS: List[ModelConfig] = [
    ModelConfig(
        name="GPT-4 Turbo",
        provider="OpenAI",
        api_key_name="OPENAI_API_KEY",
        description="Latest GPT-4 model with improved performance",
        agent_class=OpenAIAgent,
        supports_thinking=False
    ),
    ModelConfig(
        name="Claude 3 Opus",
        provider="Anthropic",
        api_key_name="ANTHROPIC_API_KEY",
        description="Most capable Claude model for complex tasks",
        agent_class=AnthropicAgent,
        supports_thinking=False
    ),
    ModelConfig(
        name="Gemini Pro",
        provider="Google",
        api_key_name="GOOGLE_API_KEY",
        description="Google's latest language model with thinking process",
        agent_class=GeminiAgent,
        supports_thinking=True
    ),
    ModelConfig(
        name="Mixtral-8x7B",
        provider="Together AI",
        api_key_name="TOGETHER_API_KEY",
        description="Open source large language model by Meta",
        agent_class=TogetherAgent,
        supports_thinking=False
    ),
    ModelConfig(
        name="OpenRouter Hub",
        provider="OpenRouter",
        api_key_name="OPENROUTER_API_KEY",
        description="Access to multiple LLM providers through a single API",
        agent_class=OpenRouterAgent,
        supports_thinking=False
    )
]

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    # Load environment variables
    load_env_config()
    
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = AVAILABLE_MODELS[0]
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_agent' not in st.session_state:
        st.session_state.current_agent = None
        # Initialize the first available model with valid API key
        for model in AVAILABLE_MODELS:
            api_key = get_api_key(model.api_key_name)
            if api_key:
                create_agent(model)
                st.session_state.selected_model = model
                break

def get_current_agent() -> Optional[BaseAgent]:
    """Get the currently initialized agent"""
    return st.session_state.current_agent

def create_agent(model_config: ModelConfig) -> Optional[BaseAgent]:
    """Create and initialize a new agent instance"""
    api_key = get_api_key(model_config.api_key_name)
    if not api_key:
        return None
        
    agent = model_config.agent_class(api_key=api_key)
    st.session_state.current_agent = agent
    return agent
