from src.config.settings import (
    EXCLUDE_KEYWORDS,
    INJECTION_SERVICE_KEYWORDS,
    MEDSPA_KEYWORDS,
)
from src.models.clinic import Clinic
from src.scraper.crawler import download_homepage
from src.scraper.text_extractor import extract_text


def searchable_text(clinic: Clinic) -> str:
    return " ".join(
        [clinic.name, clinic.address, *clinic.raw_types, *clinic.business_types]
    ).lower()


def contains_injection_service(text: str) -> bool:
    return any(keyword in text for keyword in INJECTION_SERVICE_KEYWORDS)


def is_medspa(clinic: Clinic) -> bool:
    return any(keyword in searchable_text(clinic) for keyword in MEDSPA_KEYWORDS)


def qualifies_medspa(clinic: Clinic) -> bool:
    """Keep medspas only when an injection service is publicly advertised."""
    listing_text = searchable_text(clinic)
    if contains_injection_service(listing_text):
        clinic.service_qualification = "Injection service listed in Google Places"
        return True
    if not clinic.website:
        clinic.service_qualification = "Excluded: no website to confirm injections"
        return False

    homepage = download_homepage(clinic)
    if not homepage:
        clinic.service_qualification = "Excluded: website unavailable for injection check"
        return False
    if contains_injection_service(extract_text(homepage).lower()):
        clinic.service_qualification = "Injection service confirmed on website"
        return True

    clinic.service_qualification = "Excluded: no injection service found"
    return False


def should_keep(clinic: Clinic) -> bool:
    """
    Returns True if the clinic should be kept.
    """

    searchable = searchable_text(clinic)

    for keyword in EXCLUDE_KEYWORDS:
        if keyword in searchable:
            return False

    return not is_medspa(clinic) or qualifies_medspa(clinic)


def filter_businesses(clinics: list[Clinic]) -> list[Clinic]:
    """
    Removes unwanted businesses.
    """

    return [
        clinic
        for clinic in clinics
        if should_keep(clinic)
    ]
