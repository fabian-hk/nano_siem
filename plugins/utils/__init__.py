from typing import Tuple
import logging
import os

import geoip2.database
import ipaddress
from geoip2.errors import AddressNotFoundError

logger = logging.getLogger(__name__)


def str_to_int(s: str):
    try:
        return int(s)
    except ValueError:
        return None


geoip2_default_path = "/var/nano_siem/geolite2"


def ip_to_coordinates(input: str) -> Tuple[float, float, str, str, str]:
    geolite2_city_db_path = (
        f"{os.getenv('GEOLITE2_PATH', geoip2_default_path)}/GeoLite2-City.mmdb"
    )
    geolite2_asn_db_path = (
        f"{os.getenv('GEOLITE2_PATH', geoip2_default_path)}/GeoLite2-ASN.mmdb"
    )

    try:
        input_ip = ipaddress.ip_address(input)
        private_ip_coordinates_raw = os.getenv("PRIVATE_IP_LOCATION_INFO")
        if input_ip.is_private and private_ip_coordinates_raw:
            private_ip_coordinates = private_ip_coordinates_raw.split(",")
            if len(private_ip_coordinates) != 5:
                logger.error(
                    "PRIVATE_IP_LOCATION_INFO does not provide enough information. "
                    "It should have the format: "
                    "Longitude,Latitude,City,Country,autonomous_system_organization"
                )
            return (
                float(private_ip_coordinates[0]),
                float(private_ip_coordinates[1]),
                private_ip_coordinates[2],
                private_ip_coordinates[3],
                private_ip_coordinates[4],
            )

        with geoip2.database.Reader(geolite2_city_db_path) as reader:
            city_response = reader.city(input)

        with geoip2.database.Reader(geolite2_asn_db_path) as reader:
            asn_response = reader.asn(input)
        return (
            city_response.location.latitude,
            city_response.location.longitude,
            city_response.city.name,
            city_response.country.name,
            asn_response.autonomous_system_organization,
        )
    except (ValueError, AddressNotFoundError) as e:
        logger.error(f"Error getting coordinates: {e}")
        return None, None, None, None, None
