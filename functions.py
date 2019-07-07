#!/usr/bin/env python3

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from pathlib import Path

# disable SSL warnings, because we're secure :p
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# TOS constants
TOS_URL = "https://uvo1h5jsg8i6bcu23s8.vm.cld.sr"

# SecureTrack constants
ST_SESSION = requests.Session()
ST_SESSION.auth = ("admin", "password")
ST_SESSION.headers["Accept"] = "application/json"
ST_SESSION.verify = False

# SecureChange constants
SC_SESSION = requests.Session()
SC_SESSION.auth = ("r", "password")
SC_SESSION.headers["Accept"] = "application/json"
SC_SESSION.verify = False


def get_device(device_name: str):
    """
    Get the details of a specific device
    """
    r = ST_SESSION.get(
        f"{TOS_URL}/securetrack/api/devices", params={"name": device_name}
    )
    if r.ok:
        for device in r.json()["devices"]["device"]:
            if device["name"] == device_name:
                return device
    else:
        raise ValueError(f"Could not get {device_name}, got response {r.text}")


def get_rules(device_id: int):
    """
    Get all rules for a specific device_id
    """
    r = ST_SESSION.get(f"{TOS_URL}/securetrack/api/devices/{device_id}/rules")
    if r.ok:
        return r.json()["rules"]["rule"]
    else:
        raise ValueError(f"Could not get rules for {device_id}, got response {r.text}")


def load_ticket_template():
    """
    Load a JSON ticket template
    """
    return json.load(Path("post.json").open())


def post_ticket(ticket_dict):
    """
    Post a ticket to SecureChange
    """
    r = SC_SESSION.post(
        f"{TOS_URL}/securechangeworkflow/api/securechange/tickets", json=ticket_dict
    )
    if r.ok:
        return r.headers["Location"]
    else:
        raise ValueError("Could not post ticket, got response {r.text}")


def main():
    """
    Tests
    """
    assert get_device("SRX")["id"] == "5"
    assert len(get_rules(5)) == 10
    assert load_ticket_template()["ticket"]["subject"] == "Example Ticket"


if __name__ == "__main__":
    main()
