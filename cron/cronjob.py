import importlib
import logging

module_name_prefix = "plugins."

logger = logging.getLogger(__name__)


def cronjob():
    logger.info("Start cronjob")
    module_name = module_name_prefix + "traefik"
    module = importlib.import_module(module_name)
    module.run()


if __name__ == '__main__':
    cronjob()
