from typing import AsyncIterator, Dict
import anthropic
from .base import BaseAgent

class AnthropicAgent(BaseAgent):
    def _initialize(self) -> None:
        self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
        self._model = "claude-3-opus-20240229"  # Default to latest model
        
    async def stream_chat(self, prompt: str, **kwargs) -> AsyncIterator[Dict[str, str]]:
        thinking = ""
        response = ""
        processing_thinking = True
        
        try:
            message = await self.client.messages.create(
                model=self._model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            
            async for chunk in message:
                print(f"Received chunk: {chunk}")  # Debug log
                # Handle message content based on event type
                if chunk.type == "message_start":
                    print("Message started")
                elif chunk.type == "content_block_start":
                    print("Content block started")
                elif chunk.type == "content_block_delta":
                    if hasattr(chunk.delta, 'text'):
                        text = chunk.delta.text
                        print(f"Extracted content: {text}")  # Debug log
                        response += text
                        yield {
                            "thinking": "",
                            "response": response
                        }
                elif chunk.type == "message_delta":
                    if hasattr(chunk.delta, 'text'):
                        text = chunk.delta.text
                        print(f"Extracted content from delta: {text}")  # Debug log
                        response += text
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
