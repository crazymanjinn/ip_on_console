#!/usr/bin/env python3
from pathlib import Path
from tabulate import tabulate
import argparse
import json
import subprocess
import sys


def get_interfaces():
    try:
        ret = subprocess.run(["ip", "-j", "addr", "show", "up"],
                             capture_output=True,
                             check=True)
    except subprocess.CalledProcessError as e:
        print((f"Encountered error running cmd '{e.cmd}'; "
               f"ret: {e.returncode}, out: {e.stdout}, err: {e.stderr}"),
              file=sys.stderr)
        sys.exit(1)

    try:
        interfaces = json.loads(ret.stdout)
    except json.JSONDecodeError as e:
        print(
            f"Encountered error deserializing JSON: {e.msg}", file=sys.stderr)
        sys.exit(1)
    return interfaces


def create_table(interfaces):
    FAMILY_ROW_MAP = {"inet": 1, "inet6": 2}
    table = []
    for interface in interfaces:
        try:
            if interface["operstate"] != "UP":
                continue
        except KeyError:
            continue
        row = [interface["ifname"], "", ""]
        for addr in interface["addr_info"]:
            row[FAMILY_ROW_MAP[addr["family"]]] += (f"{addr['local']}/"
                                                    f"{addr['prefixlen']}\n")
        table.append(row)
    return tabulate(table, headers=["IFNAME", "IPv4", "IPv6"], tablefmt="psql")


def write_table(table, f):
    if f == "-":
        print(table)
        return True
    with Path(f).open("w") as f:
        f.write(table)
        f.write("\n")
        return True


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Populate IP info to /etc/issue", prog="ip_on_console")
    parser.add_argument(
        "--file",
        "-f",
        default="/etc/issue.d/01-ip.issue",
        help="write to file (default: %(default)s)",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    interfaces = get_interfaces()
    table = create_table(interfaces)
    write_table(table, args.file)
    sys.exit(0)


if __name__ == "__main__":
    main()
