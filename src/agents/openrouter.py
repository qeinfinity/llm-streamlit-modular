from typing import AsyncIterator, Dict
import openai  # OpenRouter uses OpenAI's client library
from .base import BaseAgent

class OpenRouterAgent(BaseAgent):
    def _initialize(self) -> None:
        self.client = openai.AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "https://github.com/your-username/llm-streamlit-modular",
                "X-Title": "LLM Streamlit Modular"
            }
        )
        self._model = "mistralai/mistral-nemo"  # Default model
        
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
