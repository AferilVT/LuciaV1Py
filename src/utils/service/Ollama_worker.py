import requests
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json

class OllamaWorker:
    def __init__(self, model_name="mistral", max_retries=3):
        self.base_url = "http://localhost:11434/api/generate"
        self.model_name = model_name
        
        # Configure session with retries
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
    def generate_response(self, prompt: str) -> str:
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            logging.debug(f"Sending request to Ollama with prompt: {prompt[:100]}...")
            
            response = self.session.post(self.base_url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if "error" in result:
                logging.error(f"Ollama API error: {result['error']}")
                return f"I encountered an error: {result['error']}"
                
            generated_text = result.get("response", "").strip()
            logging.debug(f"Generated response: {generated_text[:100]}...")
            return generated_text
            
        except requests.exceptions.Timeout:
            logging.error("Request to Ollama timed out")
            return "I'm sorry, but the request timed out. Please try again."
            
        except requests.exceptions.ConnectionError:
            logging.error("Failed to connect to Ollama service")
            return "I'm sorry, but I couldn't connect to the language model service. Please ensure Ollama is running."
            
        except json.JSONDecodeError:
            logging.error("Failed to parse Ollama response")
            return "I received an invalid response from the language model service."
            
        except Exception as e:
            logging.exception("Unexpected error in generate_response")
            return f"An unexpected error occurred: {str(e)}"
            
    def __del__(self):
        self.session.close()
