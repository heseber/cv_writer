"""Tests for document parsing."""

import pytest

from cv_writer.tools.document_parser import DocumentParser


def test_parse_text_file(tmp_path):
    """Test parsing a text file."""
    # Create a temporary text file
    test_file = tmp_path / "test.txt"
    test_content = "This is a test CV."
    test_file.write_text(test_content)

    # Parse the file
    result = DocumentParser.parse_file(str(test_file))
    assert result == test_content


def test_parse_markdown_file(tmp_path):
    """Test parsing a markdown file."""
    # Create a temporary markdown file
    test_file = tmp_path / "test.md"
    test_content = "# Test CV\n\nThis is a markdown CV."
    test_file.write_text(test_content)

    # Parse the file
    result = DocumentParser.parse_file(str(test_file))
    assert result == test_content


def test_parse_nonexistent_file():
    """Test parsing a nonexistent file."""
    with pytest.raises(FileNotFoundError):
        DocumentParser.parse_file("nonexistent.txt")


def test_parse_unsupported_format(tmp_path):
    """Test parsing an unsupported file format."""
    test_file = tmp_path / "test.xyz"
    test_file.write_text("test content")

    with pytest.raises(ValueError, match="Unsupported file format"):
        DocumentParser.parse_file(str(test_file))


def test_parse_multiple_files(tmp_path):
    """Test parsing multiple files."""
    # Create test files
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.md"
    file1.write_text("Content 1")
    file2.write_text("Content 2")

    # Parse multiple files
    results = DocumentParser.parse_multiple_files([str(file1), str(file2)])
    assert len(results) == 2
    assert results[0] == "Content 1"
    assert results[1] == "Content 2"
