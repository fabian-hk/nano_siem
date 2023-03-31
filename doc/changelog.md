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