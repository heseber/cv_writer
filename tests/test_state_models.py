"""Tests for state models."""

from datetime import datetime

from cv_writer.models import CVOptimizerState, ReviewFeedback


def test_review_feedback_creation():
    """Test creating ReviewFeedback."""
    feedback = ReviewFeedback(
        iteration=1,
        decision="REVISE",
        comments="Needs improvement",
    )

    assert feedback.iteration == 1
    assert feedback.decision == "REVISE"
    assert feedback.comments == "Needs improvement"
    assert isinstance(feedback.timestamp, datetime)


def test_cv_optimizer_state_defaults():
    """Test CVOptimizerState default values."""
    state = CVOptimizerState(
        job_description="Test job description",
        cv_draft="Test CV draft",
    )

    assert state.job_description == "Test job description"
    assert state.cv_draft == "Test CV draft"
    assert state.supporting_docs == []
    assert state.current_cv == ""
    assert state.iteration_count == 0
    assert state.max_iterations == 3
    assert state.feedback_history == []
    assert state.status == "INITIALIZED"
    assert state.final_decision is None
    assert state.translate_to is None
    assert state.translated_cv is None


def test_cv_optimizer_state_with_values():
    """Test CVOptimizerState with custom values."""
    state = CVOptimizerState(
        job_description="Test job",
        cv_draft="Test CV",
        supporting_docs=["Doc1", "Doc2"],
        max_iterations=5,
    )

    assert state.max_iterations == 5
    assert len(state.supporting_docs) == 2


def test_cv_optimizer_state_with_translation():
    """Test CVOptimizerState with translation fields."""
    state = CVOptimizerState(
        job_description="Test job",
        cv_draft="Test CV",
        translate_to="de",
    )

    assert state.translate_to == "de"
    assert state.translated_cv is None

    # Simulate translation
    state.translated_cv = "Übersetzter Lebenslauf"
    assert state.translated_cv == "Übersetzter Lebenslauf"


def test_feedback_history_update():
    """Test updating feedback history."""
    state = CVOptimizerState(
        job_description="Test job",
        cv_draft="Test CV",
    )

    feedback = ReviewFeedback(
        iteration=1,
        decision="REVISE",
        comments="Test feedback",
    )

    state.feedback_history.append(feedback)
    assert len(state.feedback_history) == 1
    assert state.feedback_history[0].iteration == 1
