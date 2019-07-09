#!/usr/bin/env python3

from copy import deepcopy
import json

from functions import get_device, get_rules, load_ticket_template, post_ticket


def get_rule_by_number_and_policy(rules, number, policy_name):
    """
    fill in the logic to return only the rule with the correct number, and policy_name
    """
    # logic
    # Loop through all rules for rule in rules:
    for rule in rules:
        # if the rule's rule_number doens't match, continue
        if rule["rule_number"] != number:
            continue
        # Loop through all the rule bindings
        for binding in rule["binding"]:
            # If the rule's binding policy name matches, this is the rule we want, return it
            if binding["policy"]["name"] == policy_name:
                return rule
        return rule


def update_ticket_with_rule(ticket_template, rule, management_name):
    """
    fill in logic to return an updated ticket template with the sources, destinations and services
    updated to match the rule
    make sure the default template values are not left in the dict
    """
    # logic

    # copy the ticket template we're going to use
    new_ticket_template = deepcopy(ticket_template)
    # ar_field will be access request field that we're going to mutate
    ar_field = new_ticket_template["ticket"]["steps"]["step"][0]["tasks"]["task"][0][
        "fields"
    ]["field"][0]

    # we're  going to directly mutate the sources and destinations in place
    sources = ar_field["access_request"][0]["sources"]
    destinations = ar_field["access_request"][0]["destinations"]

    # Before mutating, we'll copy one of the template objects to use as our own template
    object_template = deepcopy(sources["source"][0])

    # reset the sources and destinations to delete the default objects in the template
    sources["source"] = []
    destinations["destination"] = []

    # loop through all the src_networks in the rule and update our template object with the values
    for src in rule["src_network"]:
        ar_src = deepcopy(object_template)
        ar_src["object_name"] = src["name"]
        ar_src["management_name"] = management_name
        # add our template object to the sources of the Access Request
        sources["source"].append(ar_src)

    # do the same thing for destination
    for dst in rule["dst_network"]:
        ar_dst = deepcopy(object_template)
        ar_dst["object_name"] = dst["name"]
        print(f"3a. AR destination {dst['name']} found")
        print(f"3b. rule['dst_networks'][0]['name']")
        ar_dst["management_name"] = management_name
        destinations["destination"].append(ar_dst)

    return new_ticket_template


def add_new_service_to_ticket(ticket_template, protocol, port):
    """
    fill in logic to add a new service to a ticket template dict, and return the dict
    """
    # logic
    # copy the passed ticket_template so we can mutate it safely
    new_ticket_template = deepcopy(ticket_template)
    ar_field = new_ticket_template["ticket"]["steps"]["step"][0]["tasks"]["task"][0][
        "fields"
    ]["field"][0]
    # using the same approach for network objects above
    services = ar_field["access_request"][0]["services"]
    service_template = deepcopy(services["service"][0])

    service_template["protocol"] = protocol
    service_template["port"] = port

    # in this case, we are only Supporting adding a single service, so we can re-assign the template field
    services["service"] = [service_template]
    return new_ticket_template


def main():
    # main constants
    ticket_template = load_ticket_template()
    # program inputs are, device_name, rule_number, policy_name, protocol, port
    # the values below are just to show an example
    device_name = "CMA-R80"
    rule_number = 4
    policy_name = "Standard"
    new_protocol = "TCP"
    new_port = "8443"

    # get the device, and print it's ID
    device = get_device(device_name)
    print(f"2a. {device_name} has ID: {device['id']}")

    # get the device's rule, using it's id, and print the total
    rules = get_rules(device["id"])
    print(f"2b. {device_name} has {len(rules)} rules")

    # filter the rules to find the rule we want, and print the details
    rule = get_rule_by_number_and_policy(rules, rule_number, policy_name)

    print("2c. rule_number is the rule field we want to correlate on")

    print(f"2d. rule id is {rule['id']}, rule uid is {rule['uid']}")

    # update the ticket template with the rule values
    new_ticket_template = update_ticket_with_rule(ticket_template, rule, device_name)
    print("3c. Using object_name, and management_id to add rule objects to ticket")

    # update the ticket template with the new service values
    new_ticket_template = add_new_service_to_ticket(
        new_ticket_template, new_protocol, new_port
    )
    print("4a. Adding protocol and port to the AR services")

    # inspect the ticket template JSON
    print("5a. " + json.dumps(new_ticket_template, indent=2))
    print("5b. yes")

    # post the ticket template
    new_ticket_url = post_ticket(new_ticket_template)

    # print the new ticket's URI
    print("6a. " + new_ticket_url)


if __name__ == "__main__":
    main()
