The DigitalOcean monitors allow users to monitor the state of their DigitalOcean cloud servers (also known as Droplets). Using these monitors you can perform tasks such as detecting droplets that have been powered off or identify when a snapshot has completed.

---

## Droplet Status

The Droplet Status allows you to monitor status changes to a specified Droplet. This monitor will request the droplet status from DigitalOcean via their API, if the droplet's status matches a selected status the monitor will return True. If the returned status is not selected the monitor will return False.
