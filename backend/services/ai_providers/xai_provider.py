"""XAI Grok AI Provider implementation."""

from typing import Optional
import httpx

from .base import AIProvider, AIResponse, AIProviderError


class XAIProvider(AIProvider):
    """XAI Grok AI provider implementation."""
    
    @property
    def provider_name(self) -> str:
        return "xai"
    
    async def initialize(self) -> bool:
        """Initialize the XAI client."""
        try:
            self._client = httpx.AsyncClient(
                base_url=self.base_url or "https://api.x.ai/v1",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                timeout=30.0
            )
            return True
        except Exception as e:
            raise AIProviderError(f"Failed to initialize XAI client: {e}", self.provider_name)
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> AIResponse:
        """Generate text using XAI Grok API."""
        if not self._client:
            await self.initialize()
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs
            }
            
            response = await self._client.post("/chat/completions", json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            if "error" in data:
                raise AIProviderError(f"XAI API error: {data['error']}", self.provider_name, "api_error")
            
            choice = data["choices"][0]
            usage = data.get("usage", {})
            
            return AIResponse(
                content=choice["message"]["content"],
                provider=self.provider_name,
                model=self.model,
                usage={
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                    "total_tokens": usage.get("total_tokens", 0)
                },
                finish_reason=choice.get("finish_reason"),
                metadata={"response_id": data.get("id")}
            )
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AIProviderError(f"XAI authentication failed", self.provider_name, "auth_error")
            elif e.response.status_code == 429:
                raise AIProviderError(f"XAI rate limit exceeded", self.provider_name, "rate_limit")
            else:
                raise AIProviderError(f"XAI HTTP error: {e}", self.provider_name, "api_error")
        except Exception as e:
            raise AIProviderError(f"XAI unexpected error: {e}", self.provider_name, "unknown_error")
    
    async def health_check(self) -> bool:
        """Check XAI API health."""
        try:
            if not self._client:
                await self.initialize()
            
            # Try a minimal completion to test connectivity
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 1,
                "temperature": 0
            }
            
            response = await self._client.post("/chat/completions", json=payload)
            response.raise_for_status()
            
            data = response.json()
            return bool(data.get("choices") and data["choices"][0]["message"]["content"])
            
        except Exception:
            return False