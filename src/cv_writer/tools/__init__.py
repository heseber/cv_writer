"""Tools for document processing."""

from cv_writer.tools.document_parser import DocumentParser
from cv_writer.tools.pdf_reader import PDFReaderTool, read_pdf
from cv_writer.tools.web_scraper import WebScraperTool, scrape_web_page

__all__ = [
    "DocumentParser",
    "PDFReaderTool",
    "read_pdf",
    "WebScraperTool",
    "scrape_web_page",
]

