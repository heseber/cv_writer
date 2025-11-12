"""Tests for configuration loader."""

import os
import pytest
from pathlib import Path

from cv_writer.config import Config


def test_default_config():
    """Test default configuration values."""
    config = Config()
    assert config.llm_provider == "openai"
    assert config.llm_model == "gpt-4o"
    assert config.max_iterations == 3


def test_config_get():
    """Test getting configuration values."""
    config = Config()
    assert config.get("llm.provider") == "openai"
    assert config.get("llm.model") == "gpt-4o"
    assert config.get("nonexistent.key", "default") == "default"


def test_config_set():
    """Test setting configuration values."""
    config = Config()
    config.set("llm.provider", "anthropic")
    assert config.get("llm.provider") == "anthropic"


def test_config_from_file(tmp_path):
    """Test loading configuration from file."""
    # Create a test config file
    config_file = tmp_path / "test_config.yaml"
    config_content = """
llm:
  provider: anthropic
  model: claude-3-5-sonnet-20241022
optimizer:
  max_iterations: 5
"""
    config_file.write_text(config_content)

    # Load configuration
    config = Config(config_file=str(config_file))
    assert config.llm_provider == "anthropic"
    assert config.llm_model == "claude-3-5-sonnet-20241022"
    assert config.max_iterations == 5


def test_config_env_override(monkeypatch):
    """Test environment variable overrides."""
    # Set environment variables
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.setenv("MAX_ITERATIONS", "7")

    # Load configuration
    config = Config()
    assert config.llm_provider == "ollama"
    assert config.max_iterations == 7

