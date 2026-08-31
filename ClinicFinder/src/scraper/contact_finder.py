from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from src.utils.logger import setup_logger


logger = setup_logger()


CONTACT_KEYWORDS = [
    "contact",
    "about",
    "location",
    "locations",
    "appointment",
    "referral",
    "patient",
    "help",
    "get in touch",
]


def find_contact_links(
    soup: BeautifulSoup,
    base_url: str
) -> list[str]:
    """
    Finds possible contact-related pages.
    """

    links = []
    base_hostname = urlparse(base_url).netloc.lower().removeprefix("www.")

    if soup is None:
        return links


    for link in soup.find_all("a", href=True):

        text = link.get_text(
            " ",
            strip=True
        ).lower()

        href = link["href"].lower()


        combined = text + " " + href


        if any(
            keyword in combined
            for keyword in CONTACT_KEYWORDS
        ):

            full_url = urljoin(
                base_url,
                link["href"]
            )
            parsed = urlparse(full_url)
            hostname = parsed.netloc.lower().removeprefix("www.")
            if parsed.scheme in {"http", "https"} and hostname == base_hostname:
                links.append(full_url)


    logger.info(
        f"Found {len(links)} contact-related links"
    )


    return list(dict.fromkeys(links))


def find_facebook_links(soup: BeautifulSoup) -> list[str]:
    """Return public Facebook page links advertised by the clinic website."""
    if soup is None:
        return []

    links = []
    for link in soup.find_all("a", href=True):
        href = link["href"].strip()
        hostname = urlparse(href).netloc.lower()
        if hostname.endswith("facebook.com") or hostname.endswith("fb.com"):
            links.append(href)
    return list(dict.fromkeys(links))
