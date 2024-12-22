import google.generativeai as genai
from typing import AsyncIterator, Dict
from .base import BaseAgent

class GeminiAgent(BaseAgent):
    def _initialize(self) -> None:
        genai.configure(api_key=self.api_key)
        self._model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')

    async def stream_chat(self, prompt: str, **kwargs) -> AsyncIterator[Dict[str, str]]:
        thinking = ""
        response = ""
        processing_thinking = True
        
        try:
            response_stream = self._model.generate_content(prompt, stream=True)
            for chunk in response_stream:
                if chunk.parts:
                    if len(chunk.parts) > 1:
                        if processing_thinking:
                            thinking += chunk.parts[0].text
                            response += "".join(part.text for part in chunk.parts[1:] if part.text)
                            processing_thinking = False
                        else:
                            response += "".join(part.text for part in chunk.parts if part.text)
                    else:
                        if processing_thinking:
                            thinking += chunk.parts[0].text
                        else:
                            response += chunk.parts[0].text
                    
                    yield {
                        "thinking": thinking,
                        "response": response
                    }
                    
        except Exception as e:
            yield {
                "thinking": f"Error in thinking process: {str(e)}",
                "response": f"Error generating response: {str(e)}"
            }

    @property
    def model_name(self) -> str:
        return "Gemini-2.0-Flash-Thinking"