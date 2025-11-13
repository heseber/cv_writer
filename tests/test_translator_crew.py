"""Tests for translator crew functionality."""

from unittest.mock import Mock, patch

import pytest

from cv_writer.crews.translator_crew import TranslatorCrew


class TestTranslatorCrew:
    """Test TranslatorCrew initialization and configuration."""

    @pytest.fixture
    def mock_llm(self):
        """Create a mock LLM for testing."""
        return Mock()

    def test_translator_crew_initialization(self, mock_llm):
        """Test TranslatorCrew initializes correctly."""
        crew_instance = TranslatorCrew(mock_llm)
        assert crew_instance.llm == mock_llm
        assert crew_instance.agents_config == "config/agents.yaml"
        assert crew_instance.tasks_config == "config/tasks.yaml"

    def test_translator_crew_has_agent_method(self, mock_llm):
        """Test TranslatorCrew has cv_translator agent method."""
        crew_instance = TranslatorCrew(mock_llm)
        assert hasattr(crew_instance, "cv_translator")
        assert callable(crew_instance.cv_translator)

    def test_translator_crew_has_task_method(self, mock_llm):
        """Test TranslatorCrew has translate_cv task method."""
        crew_instance = TranslatorCrew(mock_llm)
        assert hasattr(crew_instance, "translate_cv")
        assert callable(crew_instance.translate_cv)

    def test_translator_crew_has_crew_method(self, mock_llm):
        """Test TranslatorCrew has crew method."""
        crew_instance = TranslatorCrew(mock_llm)
        assert hasattr(crew_instance, "crew")
        assert callable(crew_instance.crew)

    @patch("cv_writer.crews.translator_crew.translator_crew.Agent")
    def test_cv_translator_agent_creation(self, mock_agent_class, mock_llm):
        """Test cv_translator agent is created with correct config."""
        crew_instance = TranslatorCrew(mock_llm)
        # Call the agent method
        crew_instance.cv_translator()
        # Verify Agent was called with llm
        assert mock_agent_class.called

    @patch("cv_writer.crews.translator_crew.translator_crew.Task")
    def test_translate_cv_task_creation(self, mock_task_class, mock_llm):
        """Test translate_cv task is created correctly."""
        crew_instance = TranslatorCrew(mock_llm)
        # Call the task method
        crew_instance.translate_cv()
        # Verify Task was instantiated
        assert mock_task_class.called

