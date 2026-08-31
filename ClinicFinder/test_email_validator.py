from src.validation.email_validator import validate_email


test_emails = [

    "test@gmail.com",

    "fakeemail@notarealdomain12345.com",

    "bademail",

    "support@microsoft.com"

]


for email in test_emails:

    result = validate_email(email)

    print(
        f"{email}: {result}"
    )