from abc import ABC, abstractmethod
from typing import AsyncIterator, Dict, Optional

class BaseAgent(ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._initialize()
    
    @abstractmethod
    def _initialize(self) -> None:
        """Initialize the agent with provider-specific setup"""
        pass
    
    @abstractmethod
    async def stream_chat(self, 
        prompt: str,
        **kwargs
    ) -> AsyncIterator[Dict[str, str]]:
        """
        Stream response with thinking process and final response
        Returns: AsyncIterator yielding dicts with 'thinking' and 'response' keys
        """
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the name of the current model"""
        pass