The network availability monitors are available to perform basic network connectivity testing. These monitors will execute from the Monitoring Zone you define.

**Note:** As these monitors are being performed from our systems to your systems they are at the mercy of internet packet loss and slowness. Please keep in mind when setting up these monitors that a single failure may not indicate a true failure.

---

## TCP Port

The TCP Port monitor can be used to check the status of any TCP Port. This works by opening a TCP Socket connection to the `IP` and `Port` specified in the monitors creation form.

---

## ICMP Ping

The ICMP Ping monitor can be used to validate the status of a server by performing a single ICMP Ping request. 
