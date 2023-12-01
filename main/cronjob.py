import logging
from multiprocessing import Process

logger = logging.getLogger(__name__)

# Only for debugging purposes
if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    import os
    import django

    # Prepare Django framework to make database transaction
    os.environ["DJANGO_SETTINGS_MODULE"] = "nano_siem.settings"
    django.setup()

from plugins.overwatch import cronjob as overwatch_cronjob
from plugins.http_logs import cronjob as http_log_cronjob
from main.notifications import run as notifications


def cronjob():
    logger.info("Start cronjob")

    # Running Traefik log parsing job
    http_log_cronjob_thread = Process(target=http_log_cronjob.run)
    http_log_cronjob_thread.start()

    # Running overwatch job
    overwatch_cronjob_thread = Process(target=overwatch_cronjob.run)
    overwatch_cronjob_thread.start()

    # Running notification service
    notifications_thread = Process(target=notifications.send_notifications)
    notifications_thread.start()

    # Wait for all jobs to finish
    http_log_cronjob_thread.join()
    overwatch_cronjob_thread.join()
    notifications_thread.join()


if __name__ == "__main__":
    logger.info("Running cronjob in debug mode")
    cronjob()
