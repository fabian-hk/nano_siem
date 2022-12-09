from typing import Tuple
from pathlib import Path
import logging
import os
import urllib.request
from datetime import datetime, timedelta

import geoip2.database
import ipaddress
from geoip2.errors import AddressNotFoundError

logger = logging.getLogger(__name__)


def str_to_int(s: str):
    try:
        return int(s)
    except ValueError:
        return None


geoip2_default_path = "/home/NanoSiem/.nano_siem/geolite2"


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


def is_tor_exit_node(input: str) -> bool:
    app_folder = Path.home() / ".nano_siem"
    app_folder.mkdir(parents=True, exist_ok=True)
    tor_lst_file = app_folder / "tor_exit_nodes.txt"

    # check if file exists
    if tor_lst_file.exists():
        modified_date = datetime.fromtimestamp(tor_lst_file.stat().st_mtime)
        # download new file and replace only if exists more than a day
        if modified_date < datetime.now() - timedelta(days=1):
            urllib.request.urlretrieve(
                "https://check.torproject.org/torbulkexitlist",
                str(tor_lst_file.resolve()),
            )
    else:
        urllib.request.urlretrieve(
            "https://check.torproject.org/torbulkexitlist",
            str(tor_lst_file.resolve()),
        )

    data = tor_lst_file.read_text()
    data_into_list = data.split("\n")
    if input in data_into_list:
        return True
    else:
        return False
