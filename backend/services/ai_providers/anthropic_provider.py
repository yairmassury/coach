"""Anthropic Claude AI Provider implementation."""

from typing import Optional
import anthropic
from anthropic import AsyncAnthropic

from .base import AIProvider, AIResponse, AIProviderError


class AnthropicProvider(AIProvider):
    """Anthropic Claude AI provider implementation."""
    
    @property
    def provider_name(self) -> str:
        return "anthropic"
    
    async def initialize(self) -> bool:
        """Initialize the Anthropic client."""
        try:
            self._client = AsyncAnthropic(
                api_key=self.api_key,
                base_url=self.base_url or "https://api.anthropic.com",
                timeout=30.0
            )
            return True
        except Exception as e:
            raise AIProviderError(f"Failed to initialize Anthropic client: {e}", self.provider_name)
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> AIResponse:
        """Generate text using Anthropic Claude API."""
        if not self._client:
            await self.initialize()
        
        try:
            # Prepare message
            messages = [{"role": "user", "content": prompt}]
            
            # Create request parameters
            request_params = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs
            }
            
            # Add system prompt if provided
            if system_prompt:
                request_params["system"] = system_prompt
            
            response = await self._client.messages.create(**request_params)
            
            return AIResponse(
                content=response.content[0].text if response.content else "",
                provider=self.provider_name,
                model=self.model,
                usage={
                    "prompt_tokens": response.usage.input_tokens if response.usage else 0,
                    "completion_tokens": response.usage.output_tokens if response.usage else 0,
                    "total_tokens": (response.usage.input_tokens + response.usage.output_tokens) if response.usage else 0
                },
                finish_reason=response.stop_reason,
                metadata={"response_id": response.id}
            )
            
        except anthropic.AuthenticationError as e:
            raise AIProviderError(f"Anthropic authentication failed: {e}", self.provider_name, "auth_error")
        except anthropic.RateLimitError as e:
            raise AIProviderError(f"Anthropic rate limit exceeded: {e}", self.provider_name, "rate_limit")
        except anthropic.APIError as e:
            raise AIProviderError(f"Anthropic API error: {e}", self.provider_name, "api_error")
        except Exception as e:
            raise AIProviderError(f"Anthropic unexpected error: {e}", self.provider_name, "unknown_error")
    
    async def health_check(self) -> bool:
        """Check Anthropic Claude API health."""
        try:
            if not self._client:
                await self.initialize()
            
            # Try a minimal message to test connectivity
            response = await self._client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=1,
                temperature=0
            )
            return bool(response.content and response.content[0].text)
            
        except Exception:
            return False