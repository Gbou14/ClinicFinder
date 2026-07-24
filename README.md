## Fast clinic discovery

Run `python main.py`, enter a ZIP code, and request 10-50 results. The default
workflow finds medical candidates in a 30-mile radius, then removes duplicate
and excluded businesses (eye care and obvious med-spa/injection terms). It
exports every qualifying clinic,
including those with no email, with an `Email Status` of `Not checked` and a
`Follow-up` value of `Find email`.

Enable the existing Geocoding and Places APIs for the Google API key. Email
crawling and validation remains in
`src/pipeline/clinic_enricher.py`; it is deliberately no longer run during
fast discovery, so it can become a later enrichment pass. At the prompt, enter
`y` for **Find and validate emails now?** to run that enrichment pass for the
current batch; press Enter for the normal fast-discovery mode.

When email enrichment is enabled, the workbook keeps the results separated:
`MX-Verified Contacts` contains public addresses whose domains have MX records;
`Unverified Candidates` contains public addresses found on the clinic website
that did not pass that check. General inboxes such as `info@` and `contact@`
are preferred. Other public addresses are retained separately for review, while
career, finance, executive, privacy, and similar addresses are suppressed.

For the desktop interface, run `python gui.py`. It has the same ZIP, clinic
count, and email-enrichment controls without requiring terminal input.

The exporter includes `CRM Domain Check`. Google Places can find individual
small-practice listings, but it cannot guarantee that a website belongs only to
that location. Confirm the domain before adding it to the CRM, especially for
hospital results.

## API cost report

Every exported workbook has an `API Cost Report` sheet. It records the
Geocoding and Places Nearby Search calls made during that run and estimates the
cost after the monthly free-call cap. To make the estimate include calls made
outside this program, add the current Google Cloud monthly counts to `.env`:

```text
GOOGLE_MONTH_TO_DATE_GEOCODING=0
GOOGLE_MONTH_TO_DATE_NEARBY_SEARCH=0
```

The report defaults these values to zero, so it is not a replacement for the
Google Cloud Billing report. Website crawling and MX lookups use the clinic
websites and DNS; they do not call Geocoding or Places again.
