import os
import logging
from plugins.http_logs.models import Service

logger = logging.getLogger(__name__)


def get_service() -> Service:
    # Load configuration
    name = os.getenv("TRAEFIK_SERVICE_NAME", "Traefik")
    log_path = os.getenv("TRAEFIK_SERVICE_LOG_PATH", "/var/log/traefik_access.log")

    if Service.objects.filter(name=name).exists():
        # If service already exists update its attributes
        service = Service.objects.get(name=name)
        service.name = name
        service.log_path = log_path
        service.save()
    else:
        # If the service doesn't exist create it
        service = Service(
            name=name, type="traefik", log_position=-1, log_path=log_path, running=False
        )
        service.save()
        logger.info(f"Created new traefik job {name}")
    return service
