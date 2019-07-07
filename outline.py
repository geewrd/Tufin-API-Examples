#!/usr/bin/env python3

from copy import deepcopy  # noqa
import json

from functions import get_device, get_rules, load_ticket_template, post_ticket


def get_rule_by_number_and_policy(rules, number, policy_name):
    """
    fill in the logic to return only the rule with the correct number, and policy_name
    """
    # logic
    pass


def update_ticket_with_rule(ticket_template, rule, management_name):
    """
    fill in logic to return an updated ticket template with the sources, destinations and services
    updated to match the rule
    make sure the default template values are not left in the dict
    """
    # logic
    pass


def add_new_service_to_ticket(ticket_template, protocol, port):
    """
    fill in logic to add a new service to a ticket template dict, and return the dict
    """
    # logic
    pass


def main():
    # main constants
    ticket_template = load_ticket_template()
    # program inputs are, device_name, rule_number, policy_name, protocol, port
    device_name = ""
    rule_number = 0
    policy_name = ""
    new_protocol = ""
    new_port = ""

    # get the device by name, and print it's ID
    # get the device's rule, using it's id, and print the total
    # filter the rules to find the rule we want, and print the details
    # update the ticket template with the rule values
    # update the ticket template with the new service values
    # inspect the ticket template JSON
    # post the ticket template
    # print the new ticket's URI


if __name__ == "__main__":
    main()
