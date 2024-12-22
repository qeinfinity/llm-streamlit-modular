from typing import AsyncIterator, Dict
import aiohttp
import json
from .base import BaseAgent

class TogetherAgent(BaseAgent):
    def _initialize(self) -> None:
        self._model = "mistralai/Mixtral-8x7B-Instruct-v0.1"  # Using Mixtral as it's available in serverless
        self._api_url = "https://api.together.xyz/v1/chat/completions"
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    async def stream_chat(self, prompt: str, **kwargs) -> AsyncIterator[Dict[str, str]]:
        thinking = ""
        response = ""
        
        try:
            data = {
                "model": self._model,
                "messages": [
                    {"role": "system", "content": "You are a helpful, friendly, and knowledgeable assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1024,
                "stream": True
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self._api_url, headers=self._headers, json=data) as resp:
                    if resp.status != 200:
                        error_text = await resp.text()
                        raise Exception(f"API Error {resp.status}: {error_text}")
                    
                    async for line in resp.content:
                        if line:
                            try:
                                line = line.decode('utf-8').strip()
                                print(f"Raw line: {line}")  # Debug log
                                
                                if line.startswith('data: '):
                                    data = line[6:]  # Remove 'data: ' prefix
                                    if data != '[DONE]':
                                        chunk = json.loads(data)
                                        if chunk.get('choices') and chunk['choices'][0].get('delta', {}).get('content'):
                                            content = chunk['choices'][0]['delta']['content']
                                            response += content
                                            print(f"Added content: {content}")  # Debug log
                                        yield {
                                            "thinking": "",
                                            "response": response.strip()
                                        }
                            except json.JSONDecodeError as e:
                                print(f"JSON decode error: {e}, Line: {line}")
                                continue
                            except Exception as e:
                                print(f"Error processing chunk: {e}, Line: {line}")
                                continue
                    
        except Exception as e:
            print(f"Error in Together API: {str(e)}")  # Debug log
            yield {
                "thinking": f"Error in thinking process: {str(e)}",
                "response": f"Error generating response: {str(e)}"
            }
    
    @property
    def model_name(self) -> str:
        return self._model
