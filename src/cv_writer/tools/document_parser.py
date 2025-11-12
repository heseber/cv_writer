"""Document parsing tool for handling various file formats."""

from pathlib import Path

from cv_writer.tools.pdf_reader import read_pdf
from cv_writer.tools.web_scraper import scrape_web_page


class DocumentParser:
    """Parser for handling various document formats."""

    @staticmethod
    def parse_file(file_path: str) -> str:
        """
        Parse a file and extract its text content.

        Supports: .txt, .md, .pdf

        Args:
            file_path: Path to the file

        Returns:
            Extracted text content

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is unsupported or parsing fails
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        suffix = path.suffix.lower()

        # Handle text and markdown files
        if suffix in [".txt", ".md", ".markdown"]:
            try:
                return path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                # Try with different encoding
                return path.read_text(encoding="latin-1")

        # Handle PDF files
        elif suffix == ".pdf":
            return read_pdf(file_path)

        else:
            raise ValueError(
                f"Unsupported file format: {suffix}. "
                "Supported formats: .txt, .md, .markdown, .pdf"
            )

    @staticmethod
    def parse_source(source: str) -> str:
        """
        Parse a source that can be either a file path or URL.

        Args:
            source: File path or URL

        Returns:
            Extracted text content

        Raises:
            ValueError: If source cannot be parsed
        """
        # Check if it's a URL
        if source.startswith(("http://", "https://")):
            return scrape_web_page(source)

        # Otherwise treat as file path
        return DocumentParser.parse_file(source)

    @staticmethod
    def parse_multiple_files(file_paths: list[str]) -> list[str]:
        """
        Parse multiple files and return their contents.

        Args:
            file_paths: List of file paths

        Returns:
            List of extracted text contents

        Raises:
            ValueError: If any file cannot be parsed
        """
        contents = []
        for file_path in file_paths:
            try:
                content = DocumentParser.parse_file(file_path)
                contents.append(content)
            except Exception as e:
                raise ValueError(f"Failed to parse {file_path}: {str(e)}") from e

        return contents
