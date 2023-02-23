# All Configuration Options

In this document you can find all environment variables 
that can be used to configure the application.

## Django Settings

```bash
DJANGO_SECRET_KEY=<strong secret key with at least 50 characters>
DOMAIN_NAME=<domain name of the server>
URL=<full url e.g. https://www.example.com>

TIME_ZONE=America/Los_Angeles

INSTANCE_NAME=Main
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

## Notifications

```bash
NOTIFICATION_EMAIL=<email address>
NOTIFICATION_EMAIL_PASSWORD=<email password>
# The SMTP server has to support STARTTLS
NOTIFICATION_EMAIL_SMTP_SERVER=<smtp server>

NOTIFICATION_EMAIL_SMTP_PORT=<smtp port> # Default 587

# If you want to send emails to a different email address
NOTIFICATION_EMAIL_RECEIVER=<email address>
```

## Traefik Module

```bash
# Optional configuration
TRAEFIK_SERVICE_NAME=Traefik
TRAEFIK_SERVICE_LOG_PATH=/var/log/traefik_access.log
```

### IP Address to Coordinate Config

```bash
# Set default values for private IP addresses
PRIVATE_IP_LOCATION_INFO=65.01236,25.46816,Oulu,Finland,DNA 

# Set path to GeoLite2 database. Not needed if 
# docker image with 'GeoIP.conf' is used.
GEO_LITE2_DB_PATH=/usr/share/GeoLite2
```

## Overwatch Module

```bash
# HTTP example
OVERWATCH_0=Name,http,https://example.com
OVERWATCH_{i}=Name,http,<url>

# TCP example
OVERWATCH_1=Name,tcp,example.com,22
OVERWATCH_{i}=Name,tcp,<domain/ip>,<port>

# Ping
OVERWATCH_2=Name,ping,example.com
OVERWATCH_{i}=Name,ping,<domain/ip>

# Disk
OVERWATCH_3=Name,disk,/dev/sda1,/media/usb,58d775d2-1fcb-4d10-aee5-cb956a86abd3
OVERWATCH_{i}=Name,disk,<device>,<mount point>,<uuid>

# Configure whether to check TLS certificates for http services.
# Should be set to True but if you have a self-signed certificate
# you have to set this to 'False'.
OW_HTTP_VERIFY_SSL=True

# Configure the timeout for network service availability checks.
OW_NETWORK_TIMEOUT=10

# If your root filesystem is mounted somewhere else than the default
# mount option you have to set the path here.
OW_DISK_ROOTFS_PREFIX=/mnt/rootfs

# The default is to remove services from the database
# if they are not configured as environment variables.
# If you want to keep the services in the database
# you have to set this to 'False'.
OW_REMOVE_OLD_SERVICES=True

# Number of days to plot in the network latency plots.
# Default is 1 days. Can be a float.
OW_LATENCY_PLOT_DAYS=1

# Kernel size for smoothing the latency plot.
# Higher values will result in a smoother plot.
# Default is 60.
OW_LATENCY_PLOT_SMOOTHING=60

# Number of days to plot in the disk usage plots.
# Default is 30 days. Can be a float.
OW_DISK_PLOT_DAYS=30

# Kernel size for smoothing the disk usage plot.
# Higher values will result in a smoother plot.
# Default is 60.
OW_DISK_PLOT_SMOOTHING=60
```

# Debugging

```bash
# Enable django debugging mode
DEBUG=False

# Show debug logs from the web application and the main cronjob script
MAIN_LOG_LEVEL=DEBUG

# Show debug logs from the http_logs and overwatch module
PLUGINS_LOG_LEVEL=DEBUG

# Show debug logs from the OIDC authentication
MOZILLA_OIDC_LOG_LEVEL=DEBUG

# Show debug logs from the django framework
DJANGO_LOG_LEVEL=DEBUG
```