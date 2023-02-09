from typing import Tuple
import os
import logging

import geoip2.database
import ipaddress
from geoip2.errors import AddressNotFoundError

from plugins.http_logs.models import ServiceLog

logger = logging.getLogger(__name__)

geoip2_default_path = "/home/NanoSiem/.nano_siem/geolite2"


def ip_to_coordinates(ip: str, log_line: ServiceLog):
    geolite2_city_db_path = f"{os.getenv('GEO_LITE2_DB_PATH', geoip2_default_path)}/GeoLite2-City.mmdb"
    geolite2_asn_db_path = f"{os.getenv('GEO_LITE2_DB_PATH', geoip2_default_path)}/GeoLite2-ASN.mmdb"

    try:
        input_ip = ipaddress.ip_address(ip)
        private_ip_coordinates_raw = os.getenv("PRIVATE_IP_LOCATION_INFO")
        if input_ip.is_private and private_ip_coordinates_raw:
            private_ip_coordinates = private_ip_coordinates_raw.split(",")
            if len(private_ip_coordinates) != 5:
                logger.error(
                    "PRIVATE_IP_LOCATION_INFO does not provide enough information. "
                    "It should have the format: "
                    "Longitude,Latitude,City,Country,autonomous_system_organization"
                )
            log_line.longitude = float(private_ip_coordinates[0])
            log_line.latitude = float(private_ip_coordinates[1])
            log_line.city_name = private_ip_coordinates[2]
            log_line.country_name = private_ip_coordinates[3]
            log_line.asn = private_ip_coordinates[4]
            return

        with geoip2.database.Reader(geolite2_city_db_path) as reader:
            city_response = reader.city(ip)

        with geoip2.database.Reader(geolite2_asn_db_path) as reader:
            asn_response = reader.asn(ip)

        log_line.longitude = city_response.location.longitude
        log_line.latitude = city_response.location.latitude
        log_line.city_name = city_response.city.name
        log_line.country_name = city_response.country.name
        log_line.asn = asn_response.autonomous_system_organization
    except (ValueError, AddressNotFoundError) as e:
        logger.error(f"Error getting coordinates: {e}")
