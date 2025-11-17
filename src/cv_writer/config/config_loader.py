"""Configuration loader for CV Optimizer."""

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class with hierarchical loading."""

    # Default configuration
    DEFAULTS = {
        "llm": {
            "provider": "openai",
            "model": "gpt-4o",
            "temperature": 0.7,
        },
        "optimizer": {
            "max_iterations": 3,
            "save_intermediate_versions": False,
        },
        "output": {
            "directory": "./output",
            "cv_filename_pattern": "cv_optimized_{timestamp}.md",
            "feedback_filename_pattern": "cv_review_history_{timestamp}.md",
        },
        "translation": {
            "enabled": False,
            "target_language": None,
            "llm_provider": None,
            "llm_model": None,
        },
    }

    def __init__(self, config_file: str | None = None):
        """
        Initialize configuration with hierarchical loading.

        Priority (lowest to highest):
        1. Default values
        2. Config file
        3. Environment variables
        4. CLI arguments (handled separately)

        Args:
            config_file: Path to config file (YAML)
        """
        self.config = self._load_config(config_file)

    def _load_config(self, config_file: str | None) -> dict[str, Any]:
        """Load configuration from all sources."""
        # Start with defaults
        config = self._deep_copy_dict(self.DEFAULTS)

        # Load from config file if provided
        if config_file:
            file_config = self._load_config_file(config_file)
            config = self._merge_dicts(config, file_config)
        else:
            # Try to load default config file
            default_config_path = Path(__file__).parent / "cv_optimizer.yaml"
            if default_config_path.exists():
                file_config = self._load_config_file(str(default_config_path))
                config = self._merge_dicts(config, file_config)

        # Override with environment variables
        config = self._load_from_env(config)

        return config

    @staticmethod
    def _load_config_file(file_path: str) -> dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(file_path) as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {file_path}") from None
        except yaml.YAMLError as e:
            raise ValueError(
                f"Invalid YAML in config file {file_path}: {str(e)}"
            ) from e

    @staticmethod
    def _load_from_env(config: dict[str, Any]) -> dict[str, Any]:
        """Load configuration from environment variables."""
        # LLM configuration
        if os.getenv("LLM_PROVIDER"):
            config["llm"]["provider"] = os.getenv("LLM_PROVIDER")
        if os.getenv("LLM_MODEL"):
            config["llm"]["model"] = os.getenv("LLM_MODEL")
        if os.getenv("LLM_TEMPERATURE"):
            config["llm"]["temperature"] = float(os.getenv("LLM_TEMPERATURE"))

        # Optimizer configuration
        if os.getenv("MAX_ITERATIONS"):
            config["optimizer"]["max_iterations"] = int(os.getenv("MAX_ITERATIONS"))

        # Output configuration
        if os.getenv("OUTPUT_DIRECTORY"):
            config["output"]["directory"] = os.getenv("OUTPUT_DIRECTORY")

        # Ollama base URL
        if os.getenv("OLLAMA_BASE_URL"):
            if "ollama" not in config["llm"]:
                config["llm"]["ollama"] = {}
            config["llm"]["ollama_base_url"] = os.getenv("OLLAMA_BASE_URL")

        # Translation configuration
        if os.getenv("TRANSLATE_TO"):
            config["translation"]["target_language"] = os.getenv("TRANSLATE_TO")
            config["translation"]["enabled"] = True
        if os.getenv("TRANSLATION_LLM_PROVIDER"):
            config["translation"]["llm_provider"] = os.getenv("TRANSLATION_LLM_PROVIDER")
        if os.getenv("TRANSLATION_LLM_MODEL"):
            config["translation"]["llm_model"] = os.getenv("TRANSLATION_LLM_MODEL")

        return config

    @staticmethod
    def _merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
        """Recursively merge two dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = Config._merge_dicts(result[key], value)
            else:
                result[key] = value
        return result

    @staticmethod
    def _deep_copy_dict(d: dict[str, Any]) -> dict[str, Any]:
        """Deep copy a dictionary."""
        import copy

        return copy.deepcopy(d)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key: Configuration key (e.g., 'llm.provider')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value using dot notation.

        Args:
            key: Configuration key (e.g., 'llm.provider')
            value: Value to set
        """
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

    @property
    def llm_provider(self) -> str:
        """Get LLM provider."""
        return self.get("llm.provider", "openai")

    @property
    def llm_model(self) -> str:
        """Get LLM model."""
        return self.get("llm.model", "gpt-4o")

    @property
    def llm_temperature(self) -> float:
        """Get LLM temperature."""
        return self.get("llm.temperature", 0.7)

    @property
    def max_iterations(self) -> int:
        """Get max iterations."""
        return self.get("optimizer.max_iterations", 3)

    @property
    def output_directory(self) -> str:
        """Get output directory."""
        return self.get("output.directory", "./output")

    @property
    def cv_filename_pattern(self) -> str:
        """Get CV filename pattern."""
        return self.get("output.cv_filename_pattern", "cv_optimized_{timestamp}.md")

    @property
    def feedback_filename_pattern(self) -> str:
        """Get feedback filename pattern."""
        return self.get(
            "output.feedback_filename_pattern", "cv_review_history_{timestamp}.md"
        )

    @property
    def translation_enabled(self) -> bool:
        """Get translation enabled status."""
        return self.get("translation.enabled", False)

    @property
    def translation_target_language(self) -> str | None:
        """Get translation target language."""
        return self.get("translation.target_language", None)

    @property
    def translation_llm_provider(self) -> str | None:
        """Get translation LLM provider (None means use main LLM)."""
        return self.get("translation.llm_provider", None)

    @property
    def translation_llm_model(self) -> str | None:
        """Get translation LLM model (None means use main LLM)."""
        return self.get("translation.llm_model", None)

    def to_dict(self) -> dict[str, Any]:
        """Return configuration as dictionary."""
        return self.config.copy()
