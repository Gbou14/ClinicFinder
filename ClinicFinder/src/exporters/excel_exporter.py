import os
import pandas as pd
from urllib.parse import quote_plus

from src.models import clinic
from src.api.usage import build_usage_report
from src.utils.logger import setup_logger

logger = setup_logger()


def website_scope_status(clinic):
    """Flag records that are more likely to use a parent-system website."""
    if "hospital" in clinic.raw_types:
        return "Review: likely hospital/network domain"
    if clinic.website:
        return "Review: confirm this domain represents this location"
    return "No website listed"


def facebook_search_url(clinic):
    query = f"{clinic.name} {clinic.address} Facebook"
    return f"https://www.google.com/search?q={quote_plus(query)}"


def clinic_row(clinic):
    return {
        "Company Name": clinic.name,
        "Organization Type": ", ".join(clinic.business_types),
        "Domain": clinic.website,
        "CRM Domain Check": website_scope_status(clinic),
        "Preferred General Inbox": ", ".join(clinic.emails),
        "Other Public Address (review)": ", ".join(clinic.other_validated_emails),
        "Unverified Public Candidate": ", ".join(clinic.unverified_emails),
        "Official Facebook Page": ", ".join(clinic.facebook_pages),
        "Facebook Search": facebook_search_url(clinic),
        "Email Status": clinic.email_status,
        "Follow-up": "Find email" if not clinic.emails else "",
        "Phone": clinic.phone,
        "Street Address": clinic.address,
    }


def contact_row(clinic, email):
    row = clinic_row(clinic)
    row.update({
        "Email": email,
        "Source Page": clinic.email_sources.get(email, ""),
    })
    return row


def export_clinics_to_excel(
    clinics,
    filename="clinic_results.xlsx",
    month_to_date_usage=None,
):

    logger.info("Preparing Excel export...")

    df = pd.DataFrame([clinic_row(clinic) for clinic in clinics])
    contact_columns = list(df.columns) + ["Email", "Source Page"]
    verified_rows = [
        contact_row(clinic, email)
        for clinic in clinics
        for email in clinic.emails + clinic.other_validated_emails
    ]
    unverified_rows = [
        contact_row(clinic, email)
        for clinic in clinics
        for email in clinic.unverified_emails
    ]
    facebook_rows = [
        clinic_row(clinic)
        for clinic in clinics
        if not clinic.emails
    ]


    os.makedirs(
        "exports",
        exist_ok=True
    )


    filepath = os.path.join(
        "exports",
        filename
    )


    report_df = pd.DataFrame(build_usage_report(month_to_date_usage or {}))
    with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Clinics", index=False)
        pd.DataFrame(verified_rows, columns=contact_columns).to_excel(
            writer, sheet_name="MX-Verified Contacts", index=False
        )
        pd.DataFrame(unverified_rows, columns=contact_columns).to_excel(
            writer, sheet_name="Unverified Candidates", index=False
        )
        pd.DataFrame(facebook_rows, columns=df.columns).to_excel(
            writer, sheet_name="Facebook Follow-up", index=False
        )
        report_df.to_excel(writer, sheet_name="API Cost Report", index=False)


    logger.info(
        f"Export complete: {filepath}"
    )

    return filepath
