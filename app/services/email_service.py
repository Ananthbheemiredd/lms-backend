from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

from app.core.config import settings


class EmailService:

    @staticmethod
    async def send_email(
        to_email: str,
        subject: str,
        body: str
    ) -> bool:

        try:

            message = MIMEMultipart()

            message["From"] = (
                settings.EMAIL_FROM
            )

            message["To"] = (
                to_email
            )

            message["Subject"] = (
                subject
            )

            message.attach(
                MIMEText(
                    body,
                    "html"
                )
            )

            server = smtplib.SMTP(
                settings.SES_HOST,
                settings.SES_PORT
            )

            server.ehlo()

            server.starttls()

            server.ehlo()

            server.login(
                settings.SES_USER,
                settings.SES_PASS
            )

            server.sendmail(
                settings.EMAIL_FROM,
                to_email,
                message.as_string()
            )

            server.quit()

            print(
                f"Email sent successfully to {to_email}"
            )

            return True

        except Exception as e:

            print(
                f"Email Error: {str(e)}"
            )

            return False