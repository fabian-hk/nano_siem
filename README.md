# Nano SIEM

This is the repository for our 
Computer Security Project.
You should always develop
in a separate branch that will
be merged into the main branch
after a review.

# Configuration

## Setup

1. Mount Traefik access log to: `/var/log/traefik_access.log`
2. Setup GeoLite2 Free database:
   1. Create an account at [MAXMIND](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data?lang=en)
   2. Create License file: `GeoIP.conf`
   3. Mount license file to: `/etc/GeoIP.conf`
3. [Optional] Mount log file for crontab to: `/home/NanoSiem/crontab.log`

## Database

```bash
# Required configuration
MYSQL_DB_NAME=NanoSiem
MYSQL_USER=NanoSiem
MYSQL_PASSWORD=1234
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

## [Optional] Traefik Module

```bash
# Optional configuration
TRAEFIK_SERVICE_NAME=Traefik
TRAEFIK_SERVICE_LOG_PATH=/var/log/traefik_access.log
```

## [Optional] IP Address to Coordinate Config

```bash
# Optional configuration
GEOLITE2_PATH=/var/data

# Set default values for private IP addresses
PRIVATE_IP_LOCATION_INFO=65.01236,25.46816,Oulu,Finland,DNA 
```
