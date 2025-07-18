"""AI Provider Manager with fallback logic and automatic provider selection."""

import asyncio
import logging
from typing import Dict, List, Optional, Type
from dataclasses import dataclass

from .base import AIProvider, AIResponse, AIProviderError, ProviderConfig, AIProviderType
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from .google_provider import GoogleProvider
from .openrouter_provider import OpenRouterProvider
from .xai_provider import XAIProvider
from .ollama_provider import OllamaProvider

logger = logging.getLogger(__name__)


@dataclass
class ProviderStatus:
    """Status information for a provider."""
    name: str
    available: bool
    healthy: bool
    last_error: Optional[str] = None
    last_check: Optional[float] = None


class AIProviderManager:
    """Manages multiple AI providers with automatic fallback."""
    
    def __init__(self):
        self.providers: Dict[str, AIProvider] = {}
        self.provider_configs: Dict[str, ProviderConfig] = {}
        self.provider_classes: Dict[AIProviderType, Type[AIProvider]] = {
            AIProviderType.OPENAI: OpenAIProvider,
            AIProviderType.ANTHROPIC: AnthropicProvider,
            AIProviderType.GOOGLE: GoogleProvider,
            AIProviderType.OPENROUTER: OpenRouterProvider,
            AIProviderType.XAI: XAIProvider,
            AIProviderType.OLLAMA: OllamaProvider,
        }
        self.provider_priority: List[str] = []
        self.initialized = False
    
    def configure_from_env(self, settings) -> None:
        """Configure providers from environment settings."""
        configs = {}
        
        # OpenAI
        if hasattr(settings, 'OPENAI_API_KEY'):
            configs['openai'] = ProviderConfig(
                provider_type=AIProviderType.OPENAI,
                api_key=settings.OPENAI_API_KEY,
                model=getattr(settings, 'OPENAI_MODEL', 'gpt-4'),
                base_url=getattr(settings, 'OPENAI_BASE_URL', None)
            )
        
        # Anthropic
        if hasattr(settings, 'ANTHROPIC_API_KEY'):
            configs['anthropic'] = ProviderConfig(
                provider_type=AIProviderType.ANTHROPIC,
                api_key=settings.ANTHROPIC_API_KEY,
                model=getattr(settings, 'ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022'),
                base_url=getattr(settings, 'ANTHROPIC_BASE_URL', None)
            )
        
        # Google
        if hasattr(settings, 'GOOGLE_API_KEY'):
            configs['google'] = ProviderConfig(
                provider_type=AIProviderType.GOOGLE,
                api_key=settings.GOOGLE_API_KEY,
                model=getattr(settings, 'GOOGLE_MODEL', 'gemini-1.5-pro'),
                base_url=getattr(settings, 'GOOGLE_BASE_URL', None)
            )
        
        # OpenRouter
        if hasattr(settings, 'OPENROUTER_API_KEY'):
            configs['openrouter'] = ProviderConfig(
                provider_type=AIProviderType.OPENROUTER,
                api_key=settings.OPENROUTER_API_KEY,
                model=getattr(settings, 'OPENROUTER_MODEL', 'anthropic/claude-3.5-sonnet'),
                base_url=getattr(settings, 'OPENROUTER_BASE_URL', None)
            )
        
        # XAI
        if hasattr(settings, 'XAI_API_KEY'):
            configs['xai'] = ProviderConfig(
                provider_type=AIProviderType.XAI,
                api_key=settings.XAI_API_KEY,
                model=getattr(settings, 'XAI_MODEL', 'grok-beta'),
                base_url=getattr(settings, 'XAI_BASE_URL', None)
            )
        
        # Ollama
        if hasattr(settings, 'OLLAMA_MODEL'):
            configs['ollama'] = ProviderConfig(
                provider_type=AIProviderType.OLLAMA,
                api_key=getattr(settings, 'OLLAMA_API_KEY', 'none'),
                model=settings.OLLAMA_MODEL,
                base_url=getattr(settings, 'OLLAMA_BASE_URL', None)
            )
        
        # Set priority from settings
        priority_str = getattr(settings, 'AI_PROVIDER_PRIORITY', 'anthropic,openai,google,openrouter,xai,ollama')
        self.provider_priority = [p.strip() for p in priority_str.split(',')]
        
        # Store configurations
        self.provider_configs = configs
        
        logger.info(f"Configured {len(configs)} AI providers: {list(configs.keys())}")
        logger.info(f"Provider priority: {self.provider_priority}")
    
    async def initialize(self) -> None:
        """Initialize all configured and available providers."""
        if self.initialized:
            return
        
        for name, config in self.provider_configs.items():
            if not config.is_configured():
                logger.debug(f"Skipping {name} provider - not properly configured")
                continue
            
            try:
                provider_class = self.provider_classes[config.provider_type]
                provider = provider_class(
                    api_key=config.api_key,
                    model=config.model,
                    base_url=config.base_url
                )
                
                if provider.is_available():
                    await provider.initialize()
                    self.providers[name] = provider
                    logger.info(f"Initialized {name} provider with model {config.model}")
                else:
                    logger.debug(f"Skipping {name} provider - not available")
                    
            except Exception as e:
                logger.warning(f"Failed to initialize {name} provider: {e}")
        
        self.initialized = True
        logger.info(f"Initialized {len(self.providers)} AI providers")
    
    async def get_available_providers(self) -> List[str]:
        """Get list of available provider names in priority order."""
        if not self.initialized:
            await self.initialize()
        
        available = []
        for provider_name in self.provider_priority:
            if provider_name in self.providers:
                available.append(provider_name)
        
        # Add any remaining providers not in priority list
        for provider_name in self.providers:
            if provider_name not in available:
                available.append(provider_name)
        
        return available
    
    async def get_provider_status(self) -> Dict[str, ProviderStatus]:
        """Get status of all providers."""
        if not self.initialized:
            await self.initialize()
        
        status = {}
        for name, provider in self.providers.items():
            try:
                healthy = await provider.health_check()
                status[name] = ProviderStatus(
                    name=name,
                    available=True,
                    healthy=healthy
                )
            except Exception as e:
                status[name] = ProviderStatus(
                    name=name,
                    available=True,
                    healthy=False,
                    last_error=str(e)
                )
        
        return status
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        preferred_provider: Optional[str] = None,
        **kwargs
    ) -> AIResponse:
        """Generate text using the first available provider with fallback."""
        if not self.initialized:
            await self.initialize()
        
        if not self.providers:
            raise AIProviderError("No AI providers available", "manager", "no_providers")
        
        # Determine provider order
        provider_order = []
        
        # Try preferred provider first if specified
        if preferred_provider and preferred_provider in self.providers:
            provider_order.append(preferred_provider)
        
        # Add other providers in priority order
        available_providers = await self.get_available_providers()
        for provider_name in available_providers:
            if provider_name not in provider_order:
                provider_order.append(provider_name)
        
        last_error = None
        
        # Try each provider in order
        for provider_name in provider_order:
            if provider_name not in self.providers:
                continue
                
            provider = self.providers[provider_name]
            
            try:
                logger.debug(f"Attempting text generation with {provider_name}")
                response = await provider.generate_text(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                logger.info(f"Successfully generated text using {provider_name}")
                return response
                
            except AIProviderError as e:
                logger.warning(f"Provider {provider_name} failed: {e}")
                last_error = e
                
                # Don't retry on auth errors
                if e.error_code == "auth_error":
                    continue
                    
            except Exception as e:
                logger.warning(f"Unexpected error with provider {provider_name}: {e}")
                last_error = AIProviderError(str(e), provider_name, "unknown_error")
        
        # If we get here, all providers failed
        error_msg = f"All AI providers failed. Last error: {last_error}"
        raise AIProviderError(error_msg, "manager", "all_providers_failed")
    
    async def get_preferred_provider(self) -> Optional[str]:
        """Get the name of the first available and healthy provider."""
        if not self.initialized:
            await self.initialize()
        
        for provider_name in self.provider_priority:
            if provider_name in self.providers:
                try:
                    provider = self.providers[provider_name]
                    if await provider.health_check():
                        return provider_name
                except Exception:
                    continue
        
        return None
    
    async def cleanup(self) -> None:
        """Cleanup all providers."""
        for provider in self.providers.values():
            try:
                await provider.cleanup()
            except Exception as e:
                logger.warning(f"Error cleaning up provider: {e}")
        
        self.providers.clear()
        self.initialized = False


# Global instance
ai_provider_manager = AIProviderManager()