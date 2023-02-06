import logging
import os

# import django

# Prepare Django framework to make database transaction
# os.environ["DJANGO_SETTINGS_MODULE"] = "nano_siem.settings"
# django.setup()

from plugins.overwatch import cronjob as overwatch_cronjob
from plugins.http_logs import cronjob as traefik_cronjob
from main.notifications import run as notifications

logger = logging.getLogger(__name__)


# logger.setLevel(logging.DEBUG)


def cronjob():
    logger.info("Start cronjob")

    # Running Traefik log parsing job
    traefik_cronjob.run()

    # Running overwatch job
    overwatch_cronjob.run()

    # Send notifications, if available
    notifications.send_notifications()


if __name__ == "__main__":
    cronjob()
