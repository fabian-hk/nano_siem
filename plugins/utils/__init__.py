from typing import Tuple
import logging
import os

logger = logging.getLogger(__name__)


def str_to_int(s: str):
    try:
        return int(s)
    except ValueError:
        return None


def ip_to_coordinates(input: str) -> Tuple[float, float]:
    import geoip2.database
    import ipaddress
    from geoip2.errors import AddressNotFoundError

    geolite2_city_db_path = os.getenv('GEOLITE2_CITY_DB_PATH')

    try:
        input_ip = ipaddress.ip_address(input)
        private_ip_coordinates_raw = os.getenv("PRIVATE_IP_COORDINATES")
        if input_ip.is_private and private_ip_coordinates_raw:
            private_ip_coordinates = private_ip_coordinates_raw.split(",")
            return float(private_ip_coordinates[0]), float(private_ip_coordinates[1])
        with geoip2.database.Reader(geolite2_city_db_path) as reader:
            response = reader.city(input)
        return response.location.latitude, response.location.longitude
    except (ValueError, AddressNotFoundError) as e:
        logger.error(f"Error getting coordinates: {e}")
        return None, None
