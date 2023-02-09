import logging

from .modules import traefik

logger = logging.getLogger(__name__)


def run():
    # Run Traefik log parser if configured
    traefik.run()
