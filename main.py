from src.api.geocoder import get_coordinates
from src.api.google_places import search_nearby_places
from src.api.usage import reset_usage
from src.config.settings import (
    GOOGLE_MONTH_TO_DATE_GEOCODING,
    GOOGLE_MONTH_TO_DATE_NEARBY_SEARCH,
)
from src.exporters.excel_exporter import export_clinics_to_excel
from src.filters.business_filter import filter_businesses
from src.filters.deduplicator import remove_duplicates
from src.pipeline.clinic_enricher import enrich_clinic

from src.utils.logger import setup_logger


logger = setup_logger()


def main():

    logger.info(
        "Starting ClinicFinder..."
    )
    reset_usage()


    zip_code = input(
        "Enter ZIP code: "
    )
    target_count = int(input("How many clinics (10-50, default 20): ") or "20")
    if not 10 <= target_count <= 50:
        raise ValueError("Clinic count must be between 10 and 50.")
    enrich_emails = input(
        "Find and validate emails now? This is slower. (y/N): "
    ).strip().lower() in {"y", "yes"}


    location = get_coordinates(
        zip_code
    )


    clinics = search_nearby_places(
        location["latitude"],
        location["longitude"]
    )


    clinics = remove_duplicates(
        clinics
    )

    logger.info(
        f"After deduplication: {len(clinics)} clinics"
    )


    clinics = filter_businesses(
        clinics
    )

    logger.info(
        f"After filtering: {len(clinics)} clinics"
    )


    clinics = clinics[:target_count]

    if enrich_emails:
        logger.info("Email enrichment enabled: crawling and validating websites...")
        for clinic in clinics:
            enrich_clinic(clinic)


    print(
        f"\nFound {len(clinics)} businesses within a 30-mile radius\n"
    )


    for clinic in clinics:

        print(
            clinic.name
        )

        print(
            clinic.address
        )

        print(
            clinic.phone
        )

        print(
            clinic.website
        )

        print(
            "Email not checked"
        )

        print("---")
    export_path = export_clinics_to_excel(
        clinics,
        filename=f"{zip_code}_clinics.xlsx",
        month_to_date_usage={
            "Geocoding": GOOGLE_MONTH_TO_DATE_GEOCODING,
            "Places Nearby Search Pro": GOOGLE_MONTH_TO_DATE_NEARBY_SEARCH,
        },
    )
    logger.info(f"Saved file: {export_path}")


if __name__ == "__main__":
    main()
