from rapidfuzz import fuzz

from src.models.clinic import Clinic


NAME_THRESHOLD = 92


def are_duplicates(a: Clinic, b: Clinic) -> bool:
    """
    Returns True if two clinics are likely the same business.
    """

    # Exact same address = duplicate
    if (
        a.address
        and b.address
        and a.address.lower() == b.address.lower()
    ):
        return True

    similarity = fuzz.ratio(
        a.name.lower(),
        b.name.lower()
    )

    return similarity >= NAME_THRESHOLD


def remove_duplicates(
    clinics: list[Clinic]
) -> list[Clinic]:

    unique = []

    for clinic in clinics:

        duplicate_found = False

        for existing in unique:

            if are_duplicates(
                clinic,
                existing
            ):
                duplicate_found = True
                break

        if not duplicate_found:
            unique.append(clinic)

    return unique