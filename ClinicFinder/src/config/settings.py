import os
from dotenv import load_dotenv


load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Optional: copy the current calendar-month counts from Google Cloud Billing
# before a run. Defaults to zero, so the report otherwise covers this app only.
GOOGLE_MONTH_TO_DATE_GEOCODING = int(os.getenv("GOOGLE_MONTH_TO_DATE_GEOCODING", "0"))
GOOGLE_MONTH_TO_DATE_NEARBY_SEARCH = int(
    os.getenv("GOOGLE_MONTH_TO_DATE_NEARBY_SEARCH", "0")
)


DEFAULT_RADIUS_MILES = 30


INCLUDE_TYPES = [
    "medical clinic",
    "hospital",
    "urgent care",
    "doctor",
    "pediatrician",
    "chiropractor",
    "physical therapist",
    "dermatologist",
    "specialist"
]


EXCLUDE_KEYWORDS = [
    "veterinary",
    "veterinarian",
    "veterinary_care",
    "animal",
    "optical",
    "eye",
    "optometrist",
    "ophthalmology",
    "vision",
    "pharmacy",
    "physical therapy",
    "physical therapist",
    "physiotherapist",
    "occupational therapy",
    "occupational therapist",
    "imaging",
    "radiology",
    "mri",
    "x-ray",
    "dental",
    "dentist",
    "orthodont",
]

MEDSPA_KEYWORDS = [
    "medspa",
    "med spa",
    "aesthetics",
    "aesthetic",
    "skin care clinic",
    "spa",
]

INJECTION_SERVICE_KEYWORDS = [
    "botox",
    "injectable",
    "injection",
    "dermal filler",
    "filler",
    "dysport",
    "jeuveau",
    "juvederm",
    "restylane",
    "neurotoxin",
    "neuromodulator",
]

GOOGLE_PLACE_TYPES = [
    "spa",
    "skin_care_clinic",
    "medical_clinic",
    "doctor",
    "chiropractor",
    "medical_center",
    "hospital",
]
