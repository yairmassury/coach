"""Ollama AI Provider implementation (local models)."""

from typing import Optional
import httpx

from .base import AIProvider, AIResponse, AIProviderError


class OllamaProvider(AIProvider):
    """Ollama AI provider implementation for local models."""
    
    @property
    def provider_name(self) -> str:
        return "ollama"
    
    async def initialize(self) -> bool:
        """Initialize the Ollama client."""
        try:
            self._client = httpx.AsyncClient(
                base_url=self.base_url or "http://localhost:11434",
                timeout=60.0  # Longer timeout for local models
            )
            return True
        except Exception as e:
            raise AIProviderError(f"Failed to initialize Ollama client: {e}", self.provider_name)
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> AIResponse:
        """Generate text using Ollama API."""
        if not self._client:
            await self.initialize()
        
        try:
            # Prepare the full prompt
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"System: {system_prompt}\n\nUser: {prompt}\n\nAssistant:"
            
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    **kwargs
                }
            }
            
            response = await self._client.post("/api/generate", json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            if "error" in data:
                raise AIProviderError(f"Ollama API error: {data['error']}", self.provider_name, "api_error")
            
            return AIResponse(
                content=data.get("response", ""),
                provider=self.provider_name,
                model=self.model,
                usage={
                    "prompt_tokens": data.get("prompt_eval_count", 0),
                    "completion_tokens": data.get("eval_count", 0),
                    "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
                },
                finish_reason="stop" if data.get("done") else "length",
                metadata={
                    "total_duration": data.get("total_duration"),
                    "load_duration": data.get("load_duration"),
                    "prompt_eval_duration": data.get("prompt_eval_duration"),
                    "eval_duration": data.get("eval_duration")
                }
            )
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise AIProviderError(f"Ollama model not found: {self.model}", self.provider_name, "model_not_found")
            else:
                raise AIProviderError(f"Ollama HTTP error: {e}", self.provider_name, "api_error")
        except httpx.ConnectError as e:
            raise AIProviderError(f"Ollama connection failed - is Ollama running?", self.provider_name, "connection_error")
        except Exception as e:
            raise AIProviderError(f"Ollama unexpected error: {e}", self.provider_name, "unknown_error")
    
    async def health_check(self) -> bool:
        """Check Ollama API health."""
        try:
            if not self._client:
                await self.initialize()
            
            # Check if Ollama is running
            response = await self._client.get("/api/tags")
            response.raise_for_status()
            
            # Check if our model is available
            data = response.json()
            models = [model["name"] for model in data.get("models", [])]
            return self.model in models
            
        except Exception:
            return False
    
    def is_available(self) -> bool:
        """Ollama doesn't require an API key, just needs to be running."""
        return True  # Always consider available, health_check will verify if actually working