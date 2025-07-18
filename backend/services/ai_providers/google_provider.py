"""Google Gemini AI Provider implementation."""

from typing import Optional
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from .base import AIProvider, AIResponse, AIProviderError


class GoogleProvider(AIProvider):
    """Google Gemini AI provider implementation."""
    
    @property
    def provider_name(self) -> str:
        return "google"
    
    async def initialize(self) -> bool:
        """Initialize the Google Gemini client."""
        try:
            genai.configure(api_key=self.api_key)
            self._client = genai.GenerativeModel(
                model_name=self.model,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                }
            )
            return True
        except Exception as e:
            raise AIProviderError(f"Failed to initialize Google client: {e}", self.provider_name)
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> AIResponse:
        """Generate text using Google Gemini API."""
        if not self._client:
            await self.initialize()
        
        try:
            # Combine system prompt and user prompt
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser: {prompt}\n\nAssistant:"
            
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                **kwargs
            )
            
            response = await self._client.generate_content_async(
                full_prompt,
                generation_config=generation_config
            )
            
            # Extract usage information if available
            usage = {}
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                usage = {
                    "prompt_tokens": response.usage_metadata.prompt_token_count,
                    "completion_tokens": response.usage_metadata.candidates_token_count,
                    "total_tokens": response.usage_metadata.total_token_count
                }
            
            return AIResponse(
                content=response.text if response.text else "",
                provider=self.provider_name,
                model=self.model,
                usage=usage,
                finish_reason=response.candidates[0].finish_reason.name if response.candidates else None,
                metadata={"response_id": getattr(response, 'id', None)}
            )
            
        except Exception as e:
            # Handle specific Google API errors
            error_message = str(e)
            error_code = "unknown_error"
            
            if "API_KEY_INVALID" in error_message or "authentication" in error_message.lower():
                error_code = "auth_error"
            elif "quota" in error_message.lower() or "rate limit" in error_message.lower():
                error_code = "rate_limit"
            elif "blocked" in error_message.lower():
                error_code = "content_filter"
            
            raise AIProviderError(f"Google Gemini error: {e}", self.provider_name, error_code)
    
    async def health_check(self) -> bool:
        """Check Google Gemini API health."""
        try:
            if not self._client:
                await self.initialize()
            
            # Try a minimal generation to test connectivity
            response = await self._client.generate_content_async(
                "Hello",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1,
                    temperature=0
                )
            )
            return bool(response.text)
            
        except Exception:
            return False