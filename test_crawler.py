from src.scraper.crawler import download_homepage
from src.models.clinic import Clinic
from src.scraper.text_extractor import extract_text
from src.scraper.contact_finder import find_contact_links
from src.scraper.email_extractor import extract_emails
from src.scraper.page_crawler import download_page

def main():

    clinic = Clinic(
        name="Baptist Health",
        address="Miami, FL",
        website="https://www.baptisthealth.com"
    )


    page = download_homepage(clinic)


    if page:
        text = extract_text(page)

        emails = extract_emails(text)

        print("\nEmails found:")

        for email in emails:
            print(email)

        links = find_contact_links(page,clinic.website)
        for link in links:
            print(link)
        print("\nChecking contact pages...\n")

        for link in links[:5]:
            page = download_page(link)

        if page:

            text = extract_text(page)

            emails = extract_emails(page,text)

            if emails:
                print(
                 f"{link}:" )

                for email in emails:
                    print(email)

        print(text[:500])
        print("Website downloaded!")

        if page.title:
            print(
                page.title.text
            )

    else:
        print("Download failed")


if __name__ == "__main__":
    main()