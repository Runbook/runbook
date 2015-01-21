"""HTTP utilities for reactions."""

def ParseHeaders(headers_str):
    """Parse a string to return a dict of HTTP headers.

    Args:
        headers_str: str, string representation of HTTP header with one
          header:value pair in each line.
    Returns:
        dict, headers dict with header name as key and header value as value.
    """
    headers = {}
    for header in str.splitlines(str(headers_str)):
        header = header.strip()
        # Ignore empty lines
        if not header:
            continue
        key, value = header.split(':')
        key = key.strip()
        value = value.strip()
        assert key
        assert value
        headers[key] = value
    return headers
