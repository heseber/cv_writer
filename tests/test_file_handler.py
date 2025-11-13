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
    )

    result = FileHandler.format_feedback_history([feedback])

    assert "# CV Review History" in result
    assert "## Iteration 1" in result
    assert "REVISE" in result
    assert "Test comments" in result


def test_save_translated_cv(tmp_path):
    """Test saving translated CV content."""
    cv_content = "# Test CV\n\nDies ist ein Test-Lebenslauf."
    language_code = "de"
    base_filename = "cv_optimized_20251113_123456"
    
    result = FileHandler.save_translated_cv(
        cv_content=cv_content,
        output_dir=str(tmp_path),
        language_code=language_code,
        base_filename=base_filename,
    )

    assert result.exists()
    assert result.suffix == ".md"
    assert result.name == f"{base_filename}_{language_code}.md"
    assert result.read_text() == cv_content


def test_save_translated_cv_custom_basename(tmp_path):
    """Test saving translated CV with custom basename."""
    cv_content = "# Test CV\n\nCeci est un CV de test."
    language_code = "fr"
    base_filename = "my_custom_cv_20251113_123456"
    
    result = FileHandler.save_translated_cv(
        cv_content=cv_content,
        output_dir=str(tmp_path),
        language_code=language_code,
        base_filename=base_filename,
    )

    assert result.exists()
    assert result.suffix == ".md"
    assert result.name == f"{base_filename}_{language_code}.md"
    assert result.read_text() == cv_content


def test_read_file(tmp_path):
    """Test reading file content."""
    test_file = tmp_path / "test.txt"
    test_content = "Test content"
    test_file.write_text(test_content)

    result = FileHandler.read_file(str(test_file))
    assert result == test_content
