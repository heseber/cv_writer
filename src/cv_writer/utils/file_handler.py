"""File handling utilities for CV Optimizer."""

from datetime import datetime
from pathlib import Path


class FileHandler:
    """Utility class for file operations."""

    @staticmethod
    def ensure_directory(directory: str) -> Path:
        """
        Ensure directory exists, create if it doesn't.

        Args:
            directory: Directory path

        Returns:
            Path object for directory
        """
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def save_cv(
        cv_content: str,
        output_dir: str,
        filename_pattern: str = "cv_optimized_{timestamp}.md",
    ) -> Path:
        """
        Save CV content to file.

        Args:
            cv_content: CV markdown content
            output_dir: Output directory
            filename_pattern: Filename pattern with {timestamp} placeholder

        Returns:
            Path to saved file
        """
        # Ensure output directory exists
        dir_path = FileHandler.ensure_directory(output_dir)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filename_pattern.format(timestamp=timestamp)
        file_path = dir_path / filename

        # Save content
        file_path.write_text(cv_content, encoding="utf-8")

        return file_path

    @staticmethod
    def save_feedback_history(
        feedback_content: str,
        output_dir: str,
        filename_pattern: str = "cv_review_history_{timestamp}.md",
    ) -> Path:
        """
        Save feedback history to file.

        Args:
            feedback_content: Feedback markdown content
            output_dir: Output directory
            filename_pattern: Filename pattern with {timestamp} placeholder

        Returns:
            Path to saved file
        """
        # Ensure output directory exists
        dir_path = FileHandler.ensure_directory(output_dir)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filename_pattern.format(timestamp=timestamp)
        file_path = dir_path / filename

        # Save content
        file_path.write_text(feedback_content, encoding="utf-8")

        return file_path

    @staticmethod
    def format_feedback_history(feedback_history: list) -> str:
        """
        Format feedback history as markdown.

        Args:
            feedback_history: List of ReviewFeedback objects

        Returns:
            Formatted markdown string
        """
        lines = ["# CV Review History\n"]

        for feedback in feedback_history:
            lines.append(f"## Iteration {feedback.iteration}")
            lines.append(
                f"**Timestamp:** {feedback.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            lines.append(f"**Decision:** {feedback.decision}\n")

            lines.append("### Comments")
            lines.append(feedback.comments + "\n")

            lines.append("---\n")

        return "\n".join(lines)

    @staticmethod
    def read_file(file_path: str) -> str:
        """
        Read file content.

        Args:
            file_path: Path to file

        Returns:
            File content

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        return path.read_text(encoding="utf-8")
