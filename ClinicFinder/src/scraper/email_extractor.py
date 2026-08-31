import re

from bs4 import BeautifulSoup

from src.utils.logger import setup_logger

from urllib.parse import unquote


logger = setup_logger()


EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9._%+-]+"
    r"@"
    r"[a-zA-Z0-9.-]+"
    r"\."
    r"[a-zA-Z]{2,}"
)


def extract_emails_from_text(
    text: str
) -> set[str]:
    """
    Extract emails from normal text.
    """

    if not text:
        return set()

    return {
        email.lower()
        for email in EMAIL_PATTERN.findall(text)
    }



def extract_emails_from_links(
    soup: BeautifulSoup
) -> set[str]:
    """
    Extract emails from mailto links.
    """

    emails = set()

    if not soup:
        return emails


    for link in soup.find_all(
        "a",
        href=True
    ):

        href = link["href"]

        if href.lower().startswith(
            "mailto:"
        ):

            email = (
                href
                .replace(
                    "mailto:",
                    ""
                )
                .split("?")[0]
            )
            email = (unquote(email).strip().strip(",;"))


            emails.add(
                email.lower()
            )

    return emails



def extract_emails(
    soup: BeautifulSoup,
    text: str
) -> list[str]:
    """
    Extract emails from HTML and text.
    """

    emails = set()

    emails.update(
        extract_emails_from_text(text)
    )

    emails.update(
        extract_emails_from_links(soup)
    )

    # Some websites place their public contact address in structured data or
    # an HTML attribute rather than visible page text.
    if soup:
        emails.update(extract_emails_from_text(str(soup)))


    logger.info(
        f"Found {len(emails)} email addresses"
    )


    return list(emails)
