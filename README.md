# Nano SIEM

This is the repository for our 
Computer Security Project.
You should always develop
in a separate branch that will
be merged into the main branch
after a review.

# Configuration

## Traefik Module

```bash
TRAEFIK_SERVICE_NAME=Traefik
TRAEFIK_SERVICE_LOG_PATH=/var/log/access.log
```

## IP Address to Coordinate Config

```bash
GEOLITE2_PATH=/var/data
PRIVATE_IP_LOCATION_INFO=65.01236,25.46816,Oulu,Finland,DNA 
```

## Database

```bash
MYSQL_DB_NAME=NanoSiem
MYSQL_USER=NanoSiem
MYSQL_PASSWORD=1234
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```
