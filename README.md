# Nano SIEM

The Nano SIEM project is a minimalistic *security information 
and event management* (SIEM) system designed for private home servers.
This project helps to get an insight into the access log file
of a Traefik reverse proxy. It does this by resolving IPs to
coordinates and displaying them on different map views. In the
screenshot below you can see an example from the detailed map.
On this map, you can click on locations and see the requests that
were made from there. The accesses are ranged by their likelihood
to be a hacking attempt. Furthermore, there is a second view
that specifically lists hacking attempts. A screenshot of this view
can be seen below as well. These functionalities help to get
a better understanding of the server's security risks.

Furthermore, the software is easy to set up and configure.
A prebuild ready-to-use Docker container can be pulled from [Docker Hub](https://hub.docker.com/r/fabianhk/nano-siem).
If you need to parse a different log file format feel free to write
a new plugin and open a pull request.

**Detailed Map View**
![Screenshot Detailed Map](doc/screenshot_detailed_map.png)

**Event View**
![Screenshot of Event View](doc/screenshot_event_view.png)

# Demo

If you want to check out the implementation with example
data you can go to the [demo/](demo/) folder.
Further instructions how to run the application
can be found there.

# Configuration

Running the application on your own server is quite easy.
You just have to follow the instruction below 
and / or look at the docker-compose file in this
repository.

## Setup

1. Pull Docker image from [Docker Hub](https://hub.docker.com/r/fabianhk/nano-siem): ``docker pull fabianhk/nano-siem``
2. Mount Traefik access log to: `/var/log/traefik_access.log`
3. Setup GeoLite2 Free database:
   1. Create an account at [MAXMIND](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data?lang=en)
   2. Create License file: `GeoIP.conf`
   3. Mount license file to: `/etc/GeoIP.conf`
4. Configure the database (see below)
5. Configure Django settings (see below)
6. Configure Overwatch Module (see below)
7. If you want to receive email notifications you have to configure the notification settings (see below)
8. [Optional] Set a default location for private IPs via the ``PRIVATE_IP_LOCATION_INFO`` environment variable
9. [Optional] Mount log file for crontab to: `/home/NanoSiem/crontab.log`

## Django Settings

```bash
# Required configuration
DJANGO_SECRET_KEY=<strong secret key with at least 50 characters>
DOMAIN_NAME=<domain name of the server>

# Optional configuration
TIME_ZONE=America/Los_Angeles
```

## Database

```bash
# Required configuration
MYSQL_DB_NAME=NanoSiem
MYSQL_USER=NanoSiem
MYSQL_PASSWORD=1234
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

## Overwatch Module

The Overwatch module checks whether a service is available or not
every minute. If a service is not available the module will send
an email notification to the configured email address (Requires
the notification settings to be configured).
You can configure as many services per type as you want
by increasing the numbers at the end of the environment variables.

```bash
# Configure TCP availability checks
OW_TCP_0=SSH Server,192.168.178.123,22
OW_TCP_{i}=<name>,<ip/domain>,<port>

# Configure HTTP availability checks
OW_HTTP_0=HTTP Server,https://example.com
OW_HTTP_{i}=<name>,<url>

# Configure Ping availability checks
OW_PING_0=Ping Server,192.168.178.123
OW_PING_{i}=<name>,<ip/domain>
```

## Notification Settings

```bash
# If not receiver email is set the email will be sent to the same email address
NOTIFICATION_EMAIL=<email address>
NOTIFICATION_EMAIL_PASSWORD=<email password>
# The SMTP server has to support STARTTLS
NOTIFICATION_EMAIL_SMTP_SERVER=<smtp server>

# Optional configuration (default 587)
NOTIFICATION_EMAIL_SMTP_PORT=<smtp port>

# Optional configuration, if you want to send emails to a different email address
NOTIFICATION_EMAIL_RECEIVER=<email address>
```

## [Optional] Traefik Module

```bash
# Optional configuration
TRAEFIK_SERVICE_NAME=Traefik
TRAEFIK_SERVICE_LOG_PATH=/var/log/traefik_access.log
```

## [Optional] IP Address to Coordinate Config

```bash
# Set default values for private IP addresses
PRIVATE_IP_LOCATION_INFO=65.01236,25.46816,Oulu,Finland,DNA 

# Optional configuration
GEOLITE2_PATH=/var/data
```
