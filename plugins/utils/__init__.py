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


def ip_to_coordinates(input: str) -> Tuple[float, float, str, str, str]:
    geolite2_city_db_path = f"{os.getenv('GEOLITE2_PATH')}/GeoLite2-City.mmdb"
    geolite2_asn_db_path = f"{os.getenv('GEOLITE2_PATH')}/GeoLite2-ASN.mmdb"

    try:
        input_ip = ipaddress.ip_address(input)
        private_ip_coordinates_raw = os.getenv("PRIVATE_IP_LOCATION_INFO")
        if input_ip.is_private and private_ip_coordinates_raw:
            private_ip_coordinates = private_ip_coordinates_raw.split(",")
            if len(private_ip_coordinates) != 5:
                logger.error("PRIVATE_IP_LOCATION_INFO does not provide enough information. "
                             "It should have the format: "
                             "Longitude,Latitude,City,Country,autonomous_system_organization")
            return (
                float(private_ip_coordinates[0]),
                float(private_ip_coordinates[1]),
                private_ip_coordinates[2],
                private_ip_coordinates[3],
                private_ip_coordinates[4]
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
            asn_response.autonomous_system_organization
        )
    except (ValueError, AddressNotFoundError) as e:
        logger.error(f"Error getting coordinates: {e}")
        return None, None, None, None, None


def is_tor_exit_node(input):
    import urllib
    import datetime
    import os
    
    #check if file exists
    if os.path.isfile("/home/vagrant/work/projects/chipwhisperer/tor_exit_nodes.txt"):
        my_file = open("/home/vagrant/work/projects/chipwhisperer/tor_exit_nodes.txt", "r")
        modified_date = datetime.datetime.fromtimestamp(os.path.getmtime('tor_exit_nodes.txt'))
        duration = today - modified_date
        # download new file and replace only if exists more than a day
        if duration.days > 1:
            urllib.request.urlretrieve("https://check.torproject.org/torbulkexitlist", "tor_exit_nodes.txt")
            my_file = open("tor_exit_nodes.txt", "r")
    else:
        my_file = open("/home/vagrant/work/projects/chipwhisperer/tor_exit_nodes.txt", "r")
    data = my_file.read()
    data_into_list = data.split("\n")
    my_file.close()
    if input in data_into_list:
        return True
    else:
        return False
