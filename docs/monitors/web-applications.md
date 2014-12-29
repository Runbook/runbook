These Monitors are designed to monitor the status of web servers and web-based applications.

---

## HTTP GET: Status Code

The **HTTP GET: Status Code** Monitor can be used to check the status of webservers and web-based applications. This Monitor works by performing an HTTP GET request to the `URL` specified.

### Domain to request

On the Monitor creation form, there is a field labeled `Domain to request`. The contents of this field will be added to the GET requests headers as the `host` header. The purpose of this header is to specify which host the HTTP GET request is for. This allows users to perform an HTTP GET request for a specific domain using an IP as the `URL`.

For example, if a user set up the domain `example.com` with round-robin DNS to `10.0.0.1` and `10.0.0.2`, any HTTP Monitor would be load balanced between these two servers. While in some cases this is fine, if the user wanted to perform a specific set of Reactions on one host but not the other this would not work. By specifying the `host` header or the `Domain to request` field in the form, a user could set up two Monitors: `http://10.0.0.1/index.htm` and `http://10.0.0.2/index.htm`.

This allows the user to request a specific domain even if it is not part of the URL itself.

### Expected response codes

This field is a multi-select field that allows you to select the HTTP status codes that you expect your application or webserver to respond with. During the execution of this Monitor we will check the HTTP status code we get in response to our GET request and if that code is not within the "Expected response codes" list, the Monitor will be marked as false.

### Timeout value

This Monitor has a timeout value of 3 seconds. If a response is not received in 3 seconds while performing the GET request, the Monitor will return false.

---

## HTTP GET: Keyword

The **HTTP GET: Keyword** Monitor allows you to perform an HTTP or HTTPS GET request on a specific page and search for a keyword. The keyword can be either a string or a regular expression. This can be used to validate that your app is serving content correctly or search the page for errors.

### Domain to request

On the Monitor creation form, there is a field labeled `Domain to request`. The contents of this field will be added to the GET requests headers as the `host` header. The purpose of this header is to specify which host the HTTP GET request is for. This allows users to perform an HTTP GET request for a specific domain using an IP as the `URL`.

For example, if a user sets up the domain `example.com` with round-robin DNS to `10.0.0.1` and `10.0.0.2`, any HTTP Monitor would be load balanced between these two servers. While in some cases this is fine, if the user wanted to perform a specific set of Reactions on one host but not the other this would not work. By specifying the `host` header or the `Domain to request` field in the form, a user could set up two Monitors: `http://10.0.0.1/index.htm` and `http://10.0.0.2/index.htm`.

This allows the user to request a specific domain even if it is not part of the URL itself.

### Is Keyword a Regular Expression

This selection field allows you to specify whether the keyword provided is in regular expression format or not. If you are not using a regular expression you should set this to false.

### Timeout value

This monitor has a timeout value of 3 seconds. If a response is not received in 3 seconds while performing the GET request, the Monitor will return false.

---

## HTTP POST

The **HTTP POST** monitor allows you to perform an HTTP/HTTPS POST request on a URL and verify the response for various attributes - Response status code, Response headers and contents.

Following is a description of various form fields and what they are used for.

### URL

_Required field._ The URL to sent the HTTP POST request. Can contain a domain name (http://example.com/form) or IP address (http://1.2.3.4/form).

### Host

_Required field._ Host header to send in the HTTP POST request. This is especially useful when your URL is an IP address. You can then send monitors against individual servers serving your domain by specifying the domain name in the Host field and using IP based URLs.

### Payload

_Optional field._ The data sent as the body of the POST request. Runbook will accept any string of data to send to your servers. However, you may need to set up an extra *Content-Type* header if your server expects that.

### Extra headers (in request)

_Optional field._ Extra headers to pass to your HTTP POST request. Put one header : value value in each line

Example:
```
Content-type: application/json
User-Agent: Runbook
```
Note that as per HTTP specification, headers are case-insensitive.

### Expected response codes

_Optional field._ Acceptable HTTP response codes from the server. Your monitor will fail if the response code returned by server doesn't match the ones specified in the list. If you do not specify any response code, runbook will consider all values (even error codes like 503) as success.

### Keyword to match

_Optional field._ Keyword to match in the actual content of HTTP response. You can provide a simple string or a regular expression. Runbook checks for the keyword in your content, not that your entire content is defined by the keyword.

### Response headers to match

_Optional field._ Runbook will verify that these headers are present in the response, otherwise the monitor will fail. Put one header:value in each line. See *Extra headers (in request)* section for example.

> Note that for the validation fields (Expected response code, Keyword to match, Response headers to match), the monitor will pass only if *all* the specified validation fields match.

---
