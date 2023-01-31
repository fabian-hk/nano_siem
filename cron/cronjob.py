import logging
import os

# import django

# Prepare Django framework to make database transaction
# os.environ["DJANGO_SETTINGS_MODULE"] = "nano_siem.settings"
# django.setup()

from plugins import traefik, overwatch
from cron import notifications

logger = logging.getLogger(__name__)

# logger.setLevel(logging.DEBUG)


def cronjob():
    logger.info("Start cronjob")

    # Running Traefik log parsing job, if configured
    traefik_service_log_path = os.getenv(
        "TRAEFIK_SERVICE_LOG_PATH", "/var/log/traefik_access.log"
    )
    if traefik.is_configured(traefik_service_log_path):
        traefik_service_name = os.getenv("TRAEFIK_SERVICE_NAME", "Traefik")
        traefik.run(traefik_service_name, traefik_service_log_path)

    # Running overwatch job, if configured
    if overwatch.is_configured():
        overwatch.run()

    # Send notifications, if available
    notifications.send_notifications()


if __name__ == "__main__":
    cronjob()
