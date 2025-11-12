"""Tests for state models."""

from datetime import datetime

from cv_writer.models import CVOptimizerState, ReviewFeedback


def test_review_feedback_creation():
    """Test creating ReviewFeedback."""
    feedback = ReviewFeedback(
        iteration=1,
        decision="REVISE",
        comments="Needs improvement",
        improvements_needed=["Add more details", "Fix formatting"],
    )

    assert feedback.iteration == 1
    assert feedback.decision == "REVISE"
    assert feedback.comments == "Needs improvement"
    assert len(feedback.improvements_needed) == 2
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
        improvements_needed=["Improvement 1"],
    )

    state.feedback_history.append(feedback)
    assert len(state.feedback_history) == 1
    assert state.feedback_history[0].iteration == 1

