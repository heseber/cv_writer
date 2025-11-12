"""Web scraping tool for extracting job descriptions from URLs."""

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    requests = None
    BeautifulSoup = None


class WebScraperTool:
    """Tool for scraping text content from web pages."""

    def __init__(self, timeout: int = 30):
        """
        Initialize web scraper.

        Args:
            timeout: Request timeout in seconds
        """
        if requests is None or BeautifulSoup is None:
            raise ValueError(
                "Required packages not installed. "
                "Install with: pip install requests beautifulsoup4"
            )
        self.timeout = timeout

    def scrape_url(self, url: str) -> str:
        """
        Scrape text content from a URL.

        Args:
            url: URL to scrape

        Returns:
            Extracted text content

        Raises:
            ValueError: If scraping fails
        """
        if not url.startswith(("http://", "https://")):
            raise ValueError(f"Invalid URL format: {url}")

        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.124 Safari/537.36"
                )
            }

            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()

            # Get text
            text = soup.get_text(separator="\n", strip=True)

            # Clean up whitespace
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            cleaned_text = "\n".join(lines)

            if not cleaned_text:
                raise ValueError(f"No text content could be extracted from URL: {url}")

            return cleaned_text

        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to fetch URL {url}: {str(e)}") from e
        except Exception as e:
            raise ValueError(f"Failed to parse content from URL {url}: {str(e)}") from e


def scrape_web_page(url: str, timeout: int = 30) -> str:
    """
    Convenience function to scrape text from a web page.

    Args:
        url: URL to scrape
        timeout: Request timeout in seconds

    Returns:
        Extracted text content
    """
    scraper = WebScraperTool(timeout=timeout)
    return scraper.scrape_url(url)
