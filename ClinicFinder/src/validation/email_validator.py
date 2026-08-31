import re
import dns.resolver

from src.utils.logger import setup_logger


logger = setup_logger()


EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9._%+-]+"
    r"@"
    r"[a-zA-Z0-9.-]+"
    r"\."
    r"[a-zA-Z]{2,}$"
)


def validate_email(email: str) -> bool:
    """
    Validate an email address.

    Checks:
    1. Email format
    2. Domain MX records

    Returns:
        True if likely valid.
        False otherwise.
    """

    if not email:
        return False


    # Check email format
    if not EMAIL_REGEX.match(email):

        logger.info(
            f"Invalid email format: {email}"
        )

        return False


    domain = email.split("@")[1]


    # Check mail server exists
    try:

        dns.resolver.resolve(
            domain,
            "MX"
        )


        logger.info(
            f"Verified email domain: {email}"
        )


        return True


    except dns.resolver.NoAnswer:

        logger.info(
            f"No MX record found: {email}"
        )

        return False


    except dns.resolver.NXDOMAIN:

        logger.info(
            f"Domain does not exist: {email}"
        )

        return False


    except Exception as e:

        logger.warning(
            f"Email validation error {email}: {e}"
        )

        return False
    