from typing import AsyncIterator, Dict
import openai
from .base import BaseAgent

class OpenAIAgent(BaseAgent):
    def _initialize(self) -> None:
        self.client = openai.AsyncOpenAI(api_key=self.api_key)
        self._model = "gpt-4-turbo-preview"  # Default model
        
    async def stream_chat(self, prompt: str, **kwargs) -> AsyncIterator[Dict[str, str]]:
        thinking = ""
        response = ""
        processing_thinking = True
        
        try:
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
            
            stream = await self.client.chat.completions.create(
                model=self._model,
                messages=messages,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    response += chunk.choices[0].delta.content
                    yield {
                        "thinking": "",
                        "response": response
                    }
                    
        except Exception as e:
            yield {
                "thinking": f"Error in thinking process: {str(e)}",
                "response": f"Error generating response: {str(e)}"
            }
    
    @property
    def model_name(self) -> str:
        return self._model
