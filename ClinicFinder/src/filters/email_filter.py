import re

from src.utils.logger import setup_logger

logger = setup_logger()


SUPPRESSED_EMAIL_KEYWORDS = [
    "volunteer",
    "donation",
    "gift",
    "career",
    "careers",
    "jobs",
    "hr",
    "humanresource",
    "privacy",
    "legal",
    "compliance",
    "research",
    "diversity",
    "inclusion",
    "marketing",
    "billing",
    "invoice",
    "payment",
    "finance",
    "cvo",
    "ceo",
    "cfo",
    "president",
    "executive"
]

GENERAL_INBOX_NAMES = {
    "info", "contact", "hello", "support", "help", "office", "admin",
    "reception", "frontdesk", "front.desk", "referrals", "referral",
    "patients", "patientservices", "patient.service", "inquiries", "enquiries",
}

GENERAL_INBOX_PREFIXES = (
    "info", "contact", "support", "help", "office", "admin", "reception",
    "frontdesk", "referral", "guestservice", "patientrep", "patientassist",
    "mychart", "newpatient",
)


def email_category(email: str) -> str:
    """Classify public addresses without treating individual mailboxes as preferred."""
    local_part = email.lower().strip().split("@", 1)[0]
    if any(keyword in local_part for keyword in SUPPRESSED_EMAIL_KEYWORDS):
        return "suppressed"
    normalized_local_part = re.sub(r"[^a-z]", "", local_part)
    if (
        local_part in GENERAL_INBOX_NAMES
        or any(normalized_local_part.startswith(prefix) for prefix in GENERAL_INBOX_PREFIXES)
    ):
        return "general"
    return "other"


def group_emails(emails: list[str]) -> dict[str, list[str]]:
    """Return distinct general, other, and suppressed public addresses."""
    grouped = {"general": [], "other": [], "suppressed": []}
    for email in sorted({email.lower().strip() for email in emails if email}):
        grouped[email_category(email)].append(email)
    return grouped


def filter_emails(emails: list[str]) -> list[str]:
    """
    Removes emails unlikely to be useful contacts.
    """

    grouped = group_emails(emails)
    for email in grouped["suppressed"]:
        logger.info(f"Suppressed email: {email}")
    return grouped["general"] + grouped["other"]
