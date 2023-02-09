import logging
import os
from threading import Thread

import django

# Prepare Django framework to make database transaction
os.environ["DJANGO_SETTINGS_MODULE"] = "nano_siem.settings"
django.setup()

from plugins.overwatch import cronjob as overwatch_cronjob
from plugins.http_logs import cronjob as http_log_cronjob
from main.notifications import run as notifications

logger = logging.getLogger(__name__)


logger.setLevel(logging.DEBUG)


def cronjob():
    logger.info("Start cronjob")

    # Running Traefik log parsing job
    http_log_cronjob_thread = Thread(target=http_log_cronjob.run)
    http_log_cronjob_thread.start()

    # Running overwatch job
    overwatch_cronjob_thread = Thread(target=overwatch_cronjob.run)
    overwatch_cronjob_thread.start()

    # Wait for all jobs to finish
    http_log_cronjob_thread.join()
    overwatch_cronjob_thread.join()

    # Send notifications, if available
    notifications.send_notifications()


if __name__ == "__main__":
    cronjob()
