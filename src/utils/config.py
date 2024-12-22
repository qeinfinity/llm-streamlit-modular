import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

def load_env_config() -> None:
    """Load environment variables from .env file"""
    env_path = Path(__file__).parents[2] / '.env'
    load_dotenv(env_path)

def get_api_key(key_name: str) -> Optional[str]:
    """Get API key from environment variables"""
    load_env_config()  # Ensure environment is loaded
    return os.getenv(key_name)
