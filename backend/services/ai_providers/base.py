"""Base AI Provider interface and common classes."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from enum import Enum


class AIProviderType(Enum):
    """Supported AI provider types."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OPENROUTER = "openrouter"
    XAI = "xai"
    OLLAMA = "ollama"


@dataclass
class AIResponse:
    """Standardized AI response format."""
    content: str
    provider: str
    model: str
    usage: Optional[Dict[str, Any]] = None
    finish_reason: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AIProviderError(Exception):
    """Base exception for AI provider errors."""
    
    def __init__(self, message: str, provider: str, error_code: Optional[str] = None):
        super().__init__(message)
        self.provider = provider
        self.error_code = error_code


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    def __init__(self, api_key: str, model: str, base_url: Optional[str] = None):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self._client = None
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name."""
        pass
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the provider client. Return True if successful."""
        pass
    
    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> AIResponse:
        """Generate text response from the AI provider."""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is healthy and accessible."""
        pass
    
    def is_available(self) -> bool:
        """Check if the provider has valid credentials."""
        return bool(self.api_key and self.api_key.strip() and 
                   not self.api_key.startswith('your-') and 
                   self.api_key != "none")
    
    async def cleanup(self):
        """Cleanup provider resources."""
        if hasattr(self._client, 'close'):
            await self._client.close()


@dataclass
class ProviderConfig:
    """Configuration for an AI provider."""
    provider_type: AIProviderType
    api_key: str
    model: str
    base_url: Optional[str] = None
    enabled: bool = True
    priority: int = 0
    timeout: int = 30
    max_retries: int = 3
    
    def is_configured(self) -> bool:
        """Check if provider is properly configured."""
        return (
            bool(self.api_key) and 
            self.api_key.strip() != "" and
            not self.api_key.startswith('your-') and
            self.api_key != "none" and
            self.enabled
        )