from dataclasses import dataclass, field


@dataclass
class Clinic:
    name: str
    address: str
    phone: str = ""
    website: str = ""
    raw_types: list[str] = field(default_factory=list)
    business_types: list[str] = field(default_factory=list)
    email: str = ""
    verified_email: bool = False
    email_sources: dict[str, str] = field(default_factory=dict)
    organization_type: str = ""
    emails: list[str] = field(default_factory=list)
    email_candidates: list[str] = field(default_factory=list)
    validated_emails: list[str] = field(default_factory=list)
    other_validated_emails: list[str] = field(default_factory=list)
    unverified_emails: list[str] = field(default_factory=list)
    facebook_pages: list[str] = field(default_factory=list)
    service_qualification: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    email_status: str = "Not checked"

    def __str__(self):
        return f"{self.name} ({self.organization_type})"
