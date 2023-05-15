from email.headerregistry import Address
from email.message import EmailMessage
from smtplib import SMTP

from .config import MAIL_HOST, MAIL_PASSWORD, MAIL_PORT, MAIL_USERNAME


def send_email(
    recipient_email, subject, plain_message, html_message, attachment_paths=None
):
    # Create an EmailMessage object
    msg = EmailMessage()

    # Set the sender and recipient headers using AddressHeader
    msg["From"] = Address(display_name="История Болезни", domain=MAIL_USERNAME)
    msg["To"] = recipient_email

    msg["Subject"] = subject

    # Set the plain text and HTML content of the message
    msg.set_content(plain_message)
    msg.add_alternative(html_message, subtype="html")

    # Attach any provided files as attachments
    if attachment_paths:
        for attachment_path in attachment_paths:
            with open(attachment_path, "rb") as file:
                file_content = file.read()
                file_name = attachment_path.split("/")[-1]  # Extract filename from path
                msg.add_attachment(
                    file_content,
                    maintype="application",
                    subtype="octet-stream",
                    filename=file_name,
                )

    # Create an SMTP session
    with SMTP(MAIL_HOST, MAIL_PORT) as server:
        server.starttls()  # Enable TLS encryption
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        print("between")
        server.send_message(msg)
