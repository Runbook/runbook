These monitors are designed to monitor the status of web servers and web based applications.

---

## HTTP GET: Status Code

The HTTP GET: Status Code monitor can be used to check the status of webservers and web based applications. This monitor works by performing an HTTP GET request to the `URL` specified.

### Domain to request

On the monitor creation form there is a field labeled `Domain to request`, the contents of this field will be added to the GET requests headers as the `host` header. The purpose of this header is to specify which host the HTTP GET request is for. This is to allow users to perform an HTTP GET request for a specific domain using an IP as the `URL`.

For example, if a user the domain `example.com` setup with round-robin DNS to `10.0.0.1` and `10.0.0.2` any HTTP monitor would be load balanced between these two servers. While in some cases this is fine, if the user wanted to perform a specific set of Reactions on one host but not the other this would not work. By specifying the `host` header or the `Domain to request` field in the form, a user could setup two monitors `http://10.0.0.1/index.htm` and `http://10.0.0.2/index.htm`. 

This allows the user to request a specific domain even if it is not part of the URL itself.

### Expected response codes

This field is a multi-select field that allows you to select the HTTP status codes that you expect your application or webserver to respond with. During the execution of this monitor we will check the HTTP status code we get in response to our GET request and if that code is not within the "Expected response codes" list, the monitor will be marked as failed.

### Timeout value

This monitor has a timeout value of 3 seconds, if while performing the GET request the response is not received in 3 seconds the monitor will return failed.

---

## HTTP GET: Keyword

The HTTP GET: Keyword monitor allows you to perform an HTTP or HTTPS GET request on a specific page and search for a keyword. The keyword can be both a string or a regular expression, this can be used to validate that your app is serving content correctly or search the page for errors.

### Domain to request

On the monitor creation form there is a field labeled `Domain to request`, the contents of this field will be added to the GET requests headers as the `host` header. The purpose of this header is to specify which host the HTTP GET request is for. This is to allow users to perform an HTTP GET request for a specific domain using an IP as the `URL`.

For example, if a user the domain `example.com` setup with round-robin DNS to `10.0.0.1` and `10.0.0.2` any HTTP monitor would be load balanced between these two servers. While in some cases this is fine, if the user wanted to perform a specific set of Reactions on one host but not the other this would not work. By specifying the `host` header or the `Domain to request` field in the form, a user could setup two monitors `http://10.0.0.1/index.htm` and `http://10.0.0.2/index.htm`. 

This allows the user to request a specific domain even if it is not part of the URL itself.

### Is Keyword a Regular Expression

This selection field allows you to specify if the keyword provided is in regular expression format or not. If you are not using a regular expression you should set this to false.

### Timeout value

This monitor has a timeout value of 3 seconds, if while performing the GET request the response is not received in 3 seconds the monitor will return failed.
