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

# If your root filesystem is mounted somewhere else than the default
# mount option you have to set the path here.
OW_DISK_ROOTFS_PREFIX=/mnt/rootfs

# The default is to remove services from the database
# if they are not configured as environment variables.
# If you want to keep the services in the database
# you have to set this to 'False'.
OW_REMOVE_OLD_SERVICES=True
```