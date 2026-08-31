import requests

from src.config.settings import GOOGLE_API_KEY
from src.api.usage import record_call


GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


def get_coordinates(zip_code: str):
    """
    Convert ZIP code into latitude and longitude.

    Args:
        zip_code: US ZIP code

    Returns:
        Dictionary containing latitude and longitude
    """

    params = {
        "address": zip_code,
        "key": GOOGLE_API_KEY
    }

    response = requests.get(
        GEOCODE_URL,
        params=params
    )

    data = response.json()

    if data["status"] != "OK":
        raise Exception(
            f"Geocoding failed: {data['status']}"
        )

    record_call("Geocoding")

    location = data["results"][0]["geometry"]["location"]

    return {
        "zip_code": zip_code,
        "latitude": location["lat"],
        "longitude": location["lng"]
    }
