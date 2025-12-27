import logging
import pathlib
from typing import Any, Dict
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.src.core.logging_utils import mask_email

logger = logging.getLogger(__name__)

class EmailSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 1025
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_ENABLED: bool = False
    EMAIL_FROM: str = "noreply@alphasam.com"

email_settings = EmailSettings()

class EmailService:
    def __init__(self):
        self.settings = email_settings
        # Path: backend/app/src/core/email_service.py -> backend/app/templates
        template_dir = pathlib.Path(__file__).parent.parent.parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def send_email(self, to_email: str, subject: str, template_name: str, context: Dict[str, Any]):
        """
        Send an email using a template (Synchronous version for Celery task).
        """
        try:
            template = self.env.get_template(template_name)
            html_content = template.render(context)
            
            if self.settings.EMAILS_ENABLED:
                import smtplib
                from email.mime.text import MIMEText
                from email.mime.multipart import MIMEMultipart

                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = self.settings.EMAIL_FROM
                msg["To"] = to_email

                part = MIMEText(html_content, "html")
                msg.attach(part)

                with smtplib.SMTP(self.settings.SMTP_HOST, self.settings.SMTP_PORT) as server:
                    # server.starttls() # Optional: based on environment, typically port 587 needs STARTTLS
                    if self.settings.SMTP_USER and self.settings.SMTP_PASSWORD:
                        server.login(self.settings.SMTP_USER, self.settings.SMTP_PASSWORD)
                    server.sendmail(self.settings.EMAIL_FROM, to_email, msg.as_string())
                
                logger.info(f"[SMTP] Email sent to {mask_email(to_email)} | Subject: {subject}")
            else:
                logger.info(f"[MOCK] Email to {mask_email(to_email)} | Subject: {subject}")
                logger.info(f"[MOCK] Body Preview: {html_content[:200]}...")
                
        except Exception as e:
            logger.error(f"Failed to send email to {mask_email(to_email)}: {e}")
            raise e

email_service = EmailService()
