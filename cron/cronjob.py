import logging
import os

import django

# Prepare Django framework to make database transaction
# os.environ["DJANGO_SETTINGS_MODULE"] = "nano_siem.settings"
# django.setup()

from plugins import traefik

logger = logging.getLogger(__name__)


# logger.setLevel(logging.DEBUG)


def cronjob():
    logger.info("Start cronjob")
    traefik_service_name = os.getenv("TRAEFIK_SERVICE_NAME", "Traefik")
    if traefik_service_name:
        logger.info(f"Found traefik log job: {traefik_service_name}")
        traefik_service_log_path = os.getenv(
            "TRAEFIK_SERVICE_LOG_PATH", "/var/log/traefik_access.log"
        )
        if not traefik_service_log_path:
            logger.error(
                f"Env variable TRAEFIK_SERVICE_LOG_PATH for job {traefik_service_name} not set"
            )
            raise FileNotFoundError("TRAEFIK_SERVICE_LOG_PATH variable not set")
        traefik.run(traefik_service_name, traefik_service_log_path)


if __name__ == "__main__":
    cronjob()
