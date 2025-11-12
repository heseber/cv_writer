"""LLM factory for creating language model instances."""

import os
from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI


class LLMFactory:
    """Factory for creating LLM instances based on provider."""

    @staticmethod
    def create_llm(
        provider: str, model: str, temperature: float = 0.7, **kwargs: Any
    ) -> Any:
        """
        Create an LLM instance based on provider.

        Args:
            provider: LLM provider (openai, anthropic, ollama)
            model: Model name
            temperature: Temperature setting
            **kwargs: Additional provider-specific arguments

        Returns:
            LLM instance

        Raises:
            ValueError: If provider is unsupported or credentials are missing
        """
        provider = provider.lower()

        if provider == "openai":
            return LLMFactory._create_openai(model, temperature, **kwargs)
        elif provider == "anthropic":
            return LLMFactory._create_anthropic(model, temperature, **kwargs)
        elif provider == "ollama":
            return LLMFactory._create_ollama(model, temperature, **kwargs)
        else:
            raise ValueError(
                f"Unsupported LLM provider: {provider}. "
                "Supported providers: openai, anthropic, ollama"
            )

    @staticmethod
    def _create_openai(model: str, temperature: float, **kwargs: Any) -> ChatOpenAI:
        """Create OpenAI LLM instance."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable not set. "
                "Please set it to use OpenAI models."
            )

        return ChatOpenAI(
            model=model, temperature=temperature, api_key=api_key, **kwargs
        )

    @staticmethod
    def _create_anthropic(
        model: str, temperature: float, **kwargs: Any
    ) -> ChatAnthropic:
        """Create Anthropic LLM instance."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable not set. "
                "Please set it to use Anthropic models."
            )

        return ChatAnthropic(
            model=model, temperature=temperature, api_key=api_key, **kwargs
        )

    @staticmethod
    def _create_ollama(model: str, temperature: float, **kwargs: Any) -> ChatOllama:
        """Create Ollama LLM instance."""
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        return ChatOllama(
            model=model, temperature=temperature, base_url=base_url, **kwargs
        )

    @staticmethod
    def validate_provider(provider: str) -> bool:
        """
        Validate if provider is supported.

        Args:
            provider: Provider name

        Returns:
            True if supported, False otherwise
        """
        return provider.lower() in ["openai", "anthropic", "ollama"]

    @staticmethod
    def get_default_model(provider: str) -> str:
        """
        Get default model for a provider.

        Args:
            provider: Provider name

        Returns:
            Default model name
        """
        defaults = {
            "openai": "gpt-4o",
            "anthropic": "claude-3-5-sonnet-20241022",
            "ollama": "llama3.1",
        }
        return defaults.get(provider.lower(), "gpt-4o")
