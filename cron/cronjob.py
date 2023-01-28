import logging
import os

import django

# Prepare Django framework to make database transaction
os.environ["DJANGO_SETTINGS_MODULE"] = "nano_siem.settings"
django.setup()

from plugins import traefik, overwatch

logger = logging.getLogger(__name__)


logger.setLevel(logging.DEBUG)


def cronjob():
    logger.info("Start cronjob")

    traefik_service_name = os.getenv("TRAEFIK_SERVICE_NAME", None)
    if traefik_service_name:
        traefik_service_log_path = os.getenv(
            "TRAEFIK_SERVICE_LOG_PATH", "/var/log/traefik_access.log"
        )
        traefik.run(traefik_service_name, traefik_service_log_path)
    if overwatch.is_configured():
        overwatch.run()


if __name__ == "__main__":
    cronjob()
