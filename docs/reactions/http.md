The HTTP reaction is designed to allow users to make standard HTTP GET or POST
requests when a monitor fails. This opens doors for users to call a wide variety
of web services which may not yet be directly supported by Runbook.

You can set the following fields on the reaction

* **HTTP Verb** - GET or POST
* **URL** - HTTP endpoint that is called.
* **Extra Headers** - Extra HTTP headers to pass to the request. Put one
header : value pair in each line.
* **Payload** - Body of the HTTP request. Only with POST request.
