# Version 0.2.0 - [tbd]

- **Breaking change:** crontab.log has to be mounted to ``/home/ubuntu/.nano_siem/crontab.log``
- Overwatch:
  - Models changed to record start date of unavailability, so run ``python manage.py migrate``
    (the docker container does it automatically)
  - Notification settings changed
    - First notification is only sent after a certain amount of time
    - Every hour a new notification is sent if there are unavailable services
  - Availability check are executed in threads
  - HTTP availability check includes a custom user agent
- Http_logs: Log parsing jobs are reseted at start of docker container (``python -m plugins.http_logs.startup``)
- Improved loading time of Events and HTTP Logs pages
- Improved UI on mobile devices
- Cronjobs are now run in processes
- Updated dependencies

# Version 0.1.0 - 31.03.2023

- Add proper fallback login if OIDC provider is not available
- **Breaking change:** Explicitly configure the OIDC provider with environment variables.
This is necessary to start the application even if the OIDC provider is not available and later
switch to the OIDC login when the provider becomes available.

# Version 0.0.0 - 26.02.2023

- Initial release for AMD64 and ARM64
- Containing:
  - Traefik log parsing
  - Visualisation of the logs on a map
  - Event view
  - Log overview
  - Overwatch module (HTTP, TCP, PING, DISK)
  - Support for OIDC authentication