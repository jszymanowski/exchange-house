from smtplib import SMTP
from typing import Any

from pydantic import BaseModel, EmailStr

from app.core.config import EmailSettings, email_settings, settings
from app.core.logger import logger
from app.decorators.perform_as_background_task import perform_as_background_task


class EmailService(BaseModel):
    recipient: EmailStr
    subject: str
    body: str

    email_settings: EmailSettings | None = None

    def model_post_init(self, __context: Any) -> None:
        self.email_settings = email_settings

    def send(self) -> None:
        if not settings.is_production:
            logger.info("Sending email is disabled in non-production environments.")
            return

        if self.email_settings is None or not self.email_settings.is_configured:
            logger.warning("Sending email is not configured. Skipping email.")
            return

        subject = self.subject
        body = self.body

        try:
            # mypy doesn't recognize that email_settings.is_configured is True means the smtp_*properties are not None
            with SMTP(self.email_settings.smtp_server, self.email_settings.smtp_port) as server:  # type: ignore
                server.starttls()
                server.login(self.email_settings.smtp_username, self.email_settings.smtp_password)  # type: ignore
                server.sendmail(self.email_settings.smtp_username, self.recipient, f"Subject: {subject}\n\n{body}")  # type: ignore
                logger.info(f"Email sent successfully to {self.recipient}")
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")

        return

    @perform_as_background_task
    def send_async(self) -> None:
        self.send()
