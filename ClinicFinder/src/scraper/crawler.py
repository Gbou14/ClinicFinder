import requests
from bs4 import BeautifulSoup

from src.models.clinic import Clinic
from src.utils.logger import setup_logger


logger = setup_logger()


def download_homepage(
    clinic: Clinic
) -> BeautifulSoup | None:
    """
    Downloads a clinic website homepage.

    Returns:
        BeautifulSoup object if successful.
        None if the request fails.
    """

    if not clinic.website:
        logger.warning(
            f"No website found for {clinic.name}"
        )
        return None


    logger.info(
        f"Downloading website: {clinic.website}"
    )


    try:

        response = requests.get(
            clinic.website,
            timeout=10,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64)"
                )
            }
        )

        response.raise_for_status()


        soup = BeautifulSoup(
            response.text,
            "lxml"
        )


        logger.info(
            f"Successfully downloaded {clinic.name}"
        )


        return soup


    except requests.RequestException as e:

        logger.error(
            f"Failed downloading {clinic.website}: {e}"
        )

        return None