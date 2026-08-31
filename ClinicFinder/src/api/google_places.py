import requests

from src.config.settings import (
    GOOGLE_API_KEY,
    GOOGLE_PLACE_TYPES
)

from src.models.clinic import Clinic
from src.api.usage import record_call

from src.utils.logger import setup_logger
logger = setup_logger()

PLACES_URL = (
    "https://places.googleapis.com/v1/places:searchNearby"
)


def convert_to_clinic(place: dict) -> Clinic:
    return Clinic(
        name=place.get("displayName", {}).get("text", ""),
        address=place.get("formattedAddress", ""),
        phone=place.get("nationalPhoneNumber", ""),
        website=place.get("websiteUri", ""),
        raw_types=place.get("types", []),
        business_types=place.get("types",[])
    )


def search_nearby_places(
    latitude: float,
    longitude: float,
    radius_meters: int = 48280
):

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": (
            "places.displayName,"
            "places.formattedAddress,"
            "places.nationalPhoneNumber,"
            "places.websiteUri,"
            "places.types"
        )
    }

    logger.info("Searching Google Places...")

    clinics = []

    # Nearby Search returns a limited result set. Search each allowed medical
    # category separately so exclusions still leave enough candidates for a
    # 10-100 clinic batch.
    for place_type in GOOGLE_PLACE_TYPES:
        body = {
            "includedTypes": [place_type],
            "maxResultCount": 20,
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": latitude,
                        "longitude": longitude
                    },
                    "radius": radius_meters
                }
            }
        }
        response = requests.post(PLACES_URL, headers=headers, json=body, timeout=30)
        response.raise_for_status()
        record_call("Places Nearby Search Pro")
        data = response.json()
        places = data.get("places", [])
        logger.info(f"{place_type}: Google Places returned {len(places)} results")
        clinics.extend(convert_to_clinic(place) for place in places)

    logger.info(
        f"Google Places returned {len(clinics)} total results")

    return clinics
