import ipaddress
import sys

import pprint
from parse import parse_log, parse_host, validate_status_code, validate_ip, validate_host, HTTP_METHODS

log_path = "first_10.txt"


# keys = [
#     "ts", "uid", "id.orig_h", "id.orig_p", "id.resp_h", "id.resp_p",
#     "trans_depth", "method", "host", "uri", "referrer", "user_agent",
#     "request_body_len", "response_body_len", "status_code", "status_msg",
#     "info_code", "info_msg", "filename", "tags", "username", "password",
#     "proxied", "orig_fuids", "orig_mime_types", "resp_fuids", "resp_mime_types"
# ]


def read_log(input=sys.stdin) -> list:
    logs = []
    for line in input:
        line = line.strip()
        if line != "":
            logs.append(parse_log(line))

    return logs


def sort_log(logs, index):
    if index > 8 or index < 0:
        raise IndexError("Index out of range")

    if index == 7:
        return logs.sort(key=lambda l: str(l[index]))

    return logs.sort(key=lambda l: l[index])


def get_entries_by_addr(logs, host) -> list | None:
    if (h := validate_ip(host)) or (h := validate_host(host)):
        return list(filter(lambda l: l[2] == h, logs))
    else:
        raise Exception("Invalid host")


def get_entries_by_code(logs, status_code):
    if not (code := validate_status_code(status_code)):
        raise ValueError("Invalid status code")

    return list(filter(lambda l: l[9] == code, logs))


def get_failed_reads(logs, join=False):
    logs_4xx = []
    logs_5xx = []

    for log in logs:
        if not log[9]:
            continue
        if 400 <= log[9] < 500:
            logs_4xx.append(log)
        elif 500 <= log[9] < 600:
            logs_5xx.append(log)

    if join:
        return logs_4xx, logs_5xx
    else:
        return logs_4xx + logs_5xx


def get_entries_by_extension(logs, extension: str) -> list:
    return [l for l in logs if l[8] and l[8].endswith(extension)]


def entry_to_dict(log):
    return {
        "ts": log[0],
        "uid": log[1],
        "id.orig_h": log[2],
        "id.orig_p": log[3],
        "id.resp_h": log[4],
        "id.resp_p": log[5],
        "method": log[6],
        "host": log[7],
        "uri": log[8],
        "status_code": log[9],
    }


def log_to_dict(logs):
    result = {}
    for log in logs:
        if not log[1] in result.keys():
            result[log[1]] = []

        result[log[1]].append(entry_to_dict(log))

    return result


def print_stats(session):
    if len(session) < 2:
        return

    # print(f"{session}")

    unique_hosts = set()
    request_counters = {}
    first_request = session[0]["ts"]
    last_request = session[0]["ts"]
    method_counters = {key: 0 for key in HTTP_METHODS}
    # method_counters["invalid"] = 0
    status_2xx_counter = 0

    for log in session:
        unique_hosts.add(log["id.orig_h"])
        unique_hosts.add(log["id.resp_h"])

        if log["host"]:
            unique_hosts.add(log["host"])

        if str(log["id.orig_h"]) in request_counters:
            request_counters[str(log["id.orig_h"])] += 1
        else:
            request_counters[str(log["id.orig_h"])] = 1

        if log["ts"] < first_request:
            first_request = log["ts"]

        if log["ts"] >= last_request:
            last_request = log["ts"]

        if log["method"]:
            method_counters[log["method"]] += 1
        # else:
        #     method_counters["invalid"] += 1

        if log["status_code"] and 200 <= log["status_code"] < 300:
            status_2xx_counter += 1

    print("IP addresses: ", end="")
    for addr in unique_hosts:
        print(f"{str(addr): >15}\t", end="")
    print()

    print("Request counts: ", end="")
    for addr in request_counters:
        print(f"{str(addr): >15}: {request_counters[addr]: <4}\t", end="")
    print()

    print(f"First request:\t{first_request}")
    print(f"Last request:\t{last_request}")

    print("Method percentage: ", end="")
    for method in method_counters:
        print(f"{method: >8}: {method_counters[method] / len(session) * 100: .2f}%\t", end="")
    print()

    print(f"Successful requests percentage: {status_2xx_counter / len(session) * 100: .2f}%")
    print()


def print_dict_entry_dates(sessions):
    for key in sessions:
        print_stats(sessions[key])


if __name__ == "__main__":
    logs = read_log()

    for i in range(10):
        print(logs[i])

    # # pprint.pprint(logs)
    # d = log_to_dict(logs)
    # print_dict_entry_dates(d)

    # d = log_to_dict(logs)
    # print_dict_entry_dates(d)
    print(get_entries_by_extension(logs, "java"))
