import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from src.utils.logger import setup_logger


logger = setup_logger()


def download_page(url: str) -> BeautifulSoup | None:
    """
    Download and parse any webpage.
    """

    logger.info(
        f"Downloading page: {url}"
    )

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64)"
                )
            }
        )

        response.raise_for_status()


        return BeautifulSoup(
            response.text,
            "lxml"
        )


    except requests.RequestException as e:

        logger.warning(
            f"Failed downloading {url}: {e}"
        )

        return None