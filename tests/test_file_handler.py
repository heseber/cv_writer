"""Tests for file handler."""

from cv_writer.models import ReviewFeedback
from cv_writer.utils.file_handler import FileHandler


def test_ensure_directory(tmp_path):
    """Test directory creation."""
    test_dir = tmp_path / "test" / "nested" / "dir"
    result = FileHandler.ensure_directory(str(test_dir))

    assert result.exists()
    assert result.is_dir()


def test_save_cv(tmp_path):
    """Test saving CV content."""
    cv_content = "# Test CV\n\nThis is a test CV."
    result = FileHandler.save_cv(
        cv_content=cv_content,
        output_dir=str(tmp_path),
        filename_pattern="test_cv_{timestamp}.md",
    )

    assert result.exists()
    assert result.suffix == ".md"
    assert result.read_text() == cv_content


def test_save_feedback_history(tmp_path):
    """Test saving feedback history."""
    feedback_content = "# Feedback\n\nTest feedback."
    result = FileHandler.save_feedback_history(
        feedback_content=feedback_content,
        output_dir=str(tmp_path),
        filename_pattern="test_feedback_{timestamp}.md",
    )

    assert result.exists()
    assert result.suffix == ".md"
    assert result.read_text() == feedback_content


def test_format_feedback_history():
    """Test formatting feedback history."""
    feedback = ReviewFeedback(
        iteration=1,
        decision="REVISE",
        comments="Test comments",
        improvements_needed=["Item 1", "Item 2"],
    )

    result = FileHandler.format_feedback_history([feedback])

    assert "# CV Review History" in result
    assert "## Iteration 1" in result
    assert "REVISE" in result
    assert "Test comments" in result
    assert "Item 1" in result
    assert "Item 2" in result


def test_read_file(tmp_path):
    """Test reading file content."""
    test_file = tmp_path / "test.txt"
    test_content = "Test content"
    test_file.write_text(test_content)

    result = FileHandler.read_file(str(test_file))
    assert result == test_content
