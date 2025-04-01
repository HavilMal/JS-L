import os
from ipaddress import IPv4Address, IPv6Address, ip_address
from urllib.parse import urlparse, ParseResult
from datetime import date

VALID_STATUS_CODES = [100, 101, 102, 103, 200, 201, 202, 203, 204, 205, 206, 207, 208, 226, 300, 301, 302, 303, 304,
                      305, 306, 307, 308, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414,
                      415, 416, 417, 418, 421, 422, 423, 424, 425, 426, 428, 429, 431, 451, 500, 501, 502, 503, 504,
                      505, 506, 507, 508, 510, 511, 100, 101, 102, 103, 200, 201, 202, 203, 204, 205, 206, 207, 208,
                      226, 300, 301, 302, 303, 304, 305, 306, 307, 308, 400, 401, 402, 403, 404, 405, 406, 407, 408,
                      409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 421, 422, 423, 424, 425, 426, 428, 429, 431,
                      451, 500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511]

HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"]


def validate_method(method) -> bool:
    return method in HTTP_METHODS


def parse_method(method) -> str:
    if method == "-":
        return ""

    if validate_method(method):
        return method
    else:
        return ""


def parse_uri(uri) -> str:
    if uri == "-":
        return ""

    return uri


def validate_ip(host) -> IPv4Address | IPv6Address | bool:
    try:
        return ip_address(host)
    except ValueError:
        return False


def validate_host(host) -> IPv4Address | IPv6Address | bool:
    if host.startswith("www."):
        return True
    else:
        return False


def parse_host(host: str) -> IPv4Address | IPv6Address | str:
    if host == "-":
        return ""

    if ip := validate_ip(host):
        return ip

    if validate_host(host):
        return host

    return ""


def validate_status_code(status_code) -> int | bool:
    try:
        value = int(status_code)
    except ValueError:
        return False

    if value in VALID_STATUS_CODES:
        return value
    else:
        return False

def parse_status_code(status_code) -> int:
    if status_code == "-":
        return 0

    if code := validate_status_code(status_code):
        return code
    else:
        return 0


def parse_log(line: str):
    l = line.split("\t")

    print(l)
    try:
        return (
            date.fromtimestamp(float(l[0])),  # ts
            l[1],  # uid
            ip_address(l[2]),  # id.orig_h
            int(l[3]),  # id.orig_p
            ip_address(l[4]),  # id.resp_h
            int(l[5]),  # id.resp_p
            parse_method(l[7]),  # method
            parse_host(l[8]),  # host
            parse_uri(l[9]),  # uri
            parse_status_code(l[14])  # status_code
        )
    except ValueError:
        raise ValueError(f"Error while parsing line: {line}")
