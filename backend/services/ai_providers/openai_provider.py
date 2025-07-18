"""OpenAI AI Provider implementation."""

import asyncio
from typing import Optional
import openai
from openai import AsyncOpenAI

from .base import AIProvider, AIResponse, AIProviderError


class OpenAIProvider(AIProvider):
    """OpenAI AI provider implementation."""
    
    @property
    def provider_name(self) -> str:
        return "openai"
    
    async def initialize(self) -> bool:
        """Initialize the OpenAI client."""
        try:
            self._client = AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url or "https://api.openai.com/v1",
                timeout=30.0
            )
            return True
        except Exception as e:
            raise AIProviderError(f"Failed to initialize OpenAI client: {e}", self.provider_name)
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> AIResponse:
        """Generate text using OpenAI API."""
        if not self._client:
            await self.initialize()
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            return AIResponse(
                content=response.choices[0].message.content,
                provider=self.provider_name,
                model=self.model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0
                },
                finish_reason=response.choices[0].finish_reason,
                metadata={"response_id": response.id}
            )
            
        except openai.AuthenticationError as e:
            raise AIProviderError(f"OpenAI authentication failed: {e}", self.provider_name, "auth_error")
        except openai.RateLimitError as e:
            raise AIProviderError(f"OpenAI rate limit exceeded: {e}", self.provider_name, "rate_limit")
        except openai.APIError as e:
            raise AIProviderError(f"OpenAI API error: {e}", self.provider_name, "api_error")
        except Exception as e:
            raise AIProviderError(f"OpenAI unexpected error: {e}", self.provider_name, "unknown_error")
    
    async def health_check(self) -> bool:
        """Check OpenAI API health."""
        try:
            if not self._client:
                await self.initialize()
            
            # Try a minimal completion to test connectivity
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=1,
                temperature=0
            )
            return bool(response.choices[0].message.content)
            
        except Exception:
            return False