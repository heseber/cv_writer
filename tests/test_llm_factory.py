"""Tests for LLM factory."""

from unittest.mock import patch

import pytest

from cv_writer.utils.llm_factory import LLMFactory


def test_validate_provider():
    """Test provider validation."""
    assert LLMFactory.validate_provider("openai") is True
    assert LLMFactory.validate_provider("anthropic") is True
    assert LLMFactory.validate_provider("ollama") is True
    assert LLMFactory.validate_provider("invalid") is False


def test_get_default_model():
    """Test getting default model for providers."""
    assert LLMFactory.get_default_model("openai") == "gpt-4o"
    assert LLMFactory.get_default_model("anthropic") == "claude-3-5-sonnet-20241022"
    assert LLMFactory.get_default_model("ollama") == "llama3.1"


def test_create_llm_unsupported_provider():
    """Test creating LLM with unsupported provider."""
    with pytest.raises(ValueError, match="Unsupported LLM provider"):
        LLMFactory.create_llm("invalid_provider", "model", temperature=0.7)


@patch.dict("os.environ", {"OPENAI_API_KEY": "test_key"})
def test_create_openai_llm():
    """Test creating OpenAI LLM."""
    llm = LLMFactory.create_llm("openai", "gpt-4o", temperature=0.7)
    assert llm is not None
    assert llm.model_name == "gpt-4o"


def test_create_openai_llm_no_key():
    """Test creating OpenAI LLM without API key."""
    with (
        patch.dict("os.environ", {}, clear=True),
        pytest.raises(ValueError, match="OPENAI_API_KEY"),
    ):
        LLMFactory.create_llm("openai", "gpt-4o", temperature=0.7)


def test_create_ollama_llm():
    """Test creating Ollama LLM (no API key required)."""
    llm = LLMFactory.create_llm("ollama", "llama3.1", temperature=0.7)
    assert llm is not None
