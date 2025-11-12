"""PDF extraction tool for CV Optimizer."""

from pathlib import Path
from typing import Optional

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


class PDFReaderTool:
    """Tool for extracting text from PDF files."""

    def extract_text(self, file_path: str) -> str:
        """
        Extract text content from a PDF file.

        Args:
            file_path: Path to the PDF file

        Returns:
            Extracted text content

        Raises:
            ValueError: If PDF extraction fails or pypdf is not installed
        """
        if PdfReader is None:
            raise ValueError(
                "pypdf is not installed. Install it with: pip install pypdf"
            )

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        if not path.suffix.lower() == ".pdf":
            raise ValueError(f"File is not a PDF: {file_path}")

        try:
            reader = PdfReader(str(path))
            text_parts = []

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

            extracted_text = "\n".join(text_parts)

            if not extracted_text.strip():
                raise ValueError(f"No text could be extracted from PDF: {file_path}")

            return extracted_text

        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF {file_path}: {str(e)}")


def read_pdf(file_path: str) -> str:
    """
    Convenience function to extract text from a PDF file.

    Args:
        file_path: Path to the PDF file

    Returns:
        Extracted text content
    """
    tool = PDFReaderTool()
    return tool.extract_text(file_path)

