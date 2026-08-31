from bs4 import BeautifulSoup

from src.utils.logger import setup_logger


logger = setup_logger()


def extract_text(
    soup: BeautifulSoup
) -> str:
    """
    Extract readable text from webpage HTML.
    """

    if soup is None:
        return ""


    text = soup.get_text(
        separator=" ",
        strip=True
    )


    logger.info(
        f"Extracted {len(text)} characters"
    )


    return text