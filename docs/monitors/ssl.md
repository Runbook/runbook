The SSL Certificate monitors are design to monitor and validate SSL certificates for web based and non-web based applications.

**Note:** All SSL monitors currently only support TLS version 1 or higher.

---

## SSL Not Expired

The SSL Not Expired monitor can be used to validate that an SSL certificate is not expired. This monitor allows you to define a custom number of days before expiration. When the expiration date is within the specified number of days the monitor will return a False status. All other times the monitor will return a True status.

---

## Verify SSL Common Name

The SSL Common Name monitor can be used to validate that the common name provided when requesting a certificate matches the expected common name. If the certificates common name does not match the exepected common name value the monitor will return a False status. Currently this monitor does not support SNI certificates.

