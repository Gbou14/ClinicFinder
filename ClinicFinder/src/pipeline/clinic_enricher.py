from src.scraper.crawler import download_homepage
from src.scraper.text_extractor import extract_text
from src.scraper.contact_finder import find_contact_links, find_facebook_links
from src.scraper.page_crawler import download_page
from src.scraper.email_extractor import extract_emails
from src.filters.email_filter import group_emails
from src.validation.email_validator import validate_email

from src.utils.logger import setup_logger


logger = setup_logger()


def enrich_clinic(clinic):
    """
    Adds website information and emails
    to a Clinic object.
    """


    if not clinic.website:

        clinic.email_status = "No website listed"

        logger.warning(
            f"No website for {clinic.name}"
        )

        return clinic


    homepage = download_homepage(
        clinic
    )


    if not homepage:

        clinic.email_status = "Website unavailable"

        return clinic


    homepage_text = extract_text(
        homepage
    )
    clinic.facebook_pages = find_facebook_links(homepage)


    pages = find_contact_links(
        homepage,
        clinic.website
    )


    email_candidates = set()


    # Check homepage
    homepage_emails = extract_emails(homepage, homepage_text)
    email_candidates.update(homepage_emails)
    clinic.email_sources.update({email: clinic.website for email in homepage_emails})


    # Check contact pages
    for page_url in pages[:10]:

        page = download_page(
            page_url
        )

        if page:

            text = extract_text(
                page
            )

            page_emails = extract_emails(page, text)
            email_candidates.update(page_emails)
            clinic.email_sources.update({email: page_url for email in page_emails})
            clinic.facebook_pages = list(dict.fromkeys(
                clinic.facebook_pages + find_facebook_links(page)
            ))


    clinic.email_candidates = sorted(email_candidates)
    verified_emails = []


    for email in email_candidates:

        if validate_email(email):

            verified_emails.append(
                email
            )


    clinic.validated_emails = sorted(verified_emails)
    verified_groups = group_emails(verified_emails)
    candidate_groups = group_emails(clinic.email_candidates)
    clinic.emails = verified_groups["general"]
    clinic.other_validated_emails = verified_groups["other"]
    clinic.unverified_emails = sorted(
        set(candidate_groups["general"] + candidate_groups["other"])
        - set(verified_emails)
    )
    clinic.email_status = (
        "MX-verified general inbox found" if clinic.emails
        else "MX-verified other public address found" if clinic.other_validated_emails
        else "No MX-verified public address found"
    )

    logger.info(
    f"{clinic.name}: "
    f"MX-verified candidates: {verified_emails}")

    logger.info(
    f"{clinic.name}: "
    f"Preferred general inboxes: {clinic.emails}")



    return clinic
