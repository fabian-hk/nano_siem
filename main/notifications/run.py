import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string

from plugins.overwatch import notifications as overwatch_notifications

logger = logging.getLogger(__name__)


def send_notifications():
    # Setup email configuration
    sender_email = os.getenv("NOTIFICATION_EMAIL", None)
    receiver_email = os.getenv("NOTIFICATION_EMAIL_RECEIVER", sender_email)
    password = os.getenv("NOTIFICATION_EMAIL_PASSWORD", None)
    smtp_server = os.getenv("NOTIFICATION_EMAIL_SMTP_SERVER", None)

    # Check if the email notification is configured
    if not sender_email or not password or not smtp_server:
        logger.warning(
            "Email notification is not configured. Need to set NOTIFICATION_EMAIL, NOTIFICATION_EMAIL_PASSWORD and "
            "NOTIFICATION_EMAIL_SMTP_SERVER environment variables."
        )
        return

    data = {}

    # Add overwatch data to the email content
    data.update(overwatch_notifications.get_notification_data())

    # If there are notifications, sent an email
    if data:
        # Prepare the email to be sent
        message = MIMEMultipart("alternative")
        message["Subject"] = "Nano SIEM Notifications"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Alternative plain text message in case the email client does not support HTML
        text = f"There are new events in the Nano SIEM system: {os.getenv('INSTANCE_NAME', 'My Nano SIEM')}"
        part1 = MIMEText(text, "plain")
        message.attach(part1)

        # Render the HTML content for the email
        data["instance_name"] = os.getenv("INSTANCE_NAME", "My Nano SIEM")
        html = render_to_string("notifications/notification_template.html", context=data)
        part2 = MIMEText(html, "html")
        message.attach(part2)

        with smtplib.SMTP(
            smtp_server,
            int(os.getenv("NOTIFICATION_EMAIL_SMTP_PORT", 587)),
        ) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            logger.info("Notification email sent")