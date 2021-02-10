#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.7 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""

import argparse
from getpass import getpass

def get_inputs():
    """
    Get the inputs for connecting to the cluster
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='user',
                        help='AIQ username')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='AIQ password')
    parser.add_argument('--search-customer', type=str.lower,
                        required=False,
                        metavar='customer name',
                        dest='search_customer',
                        help='customer name to search on')
    parser.add_argument('--search-string', type=str.lower,
                        required=False,
                        metavar='text to search for',
                        dest='search_string',
                        help='log text to search for')
    parser.add_argument('--sort-order',
                        choices=["Cluster", "Date", "Severity", "Details", "Type"],
                        required=False,
                        metavar='sort_order',
                        dest='sort_order',
                        help='column to sort on for certain script outputs')
    parser.add_argument('--node-id', type=int,
                        required=False,
                        metavar='node_id',
                        dest='node_id',
                        help='node ID required by some scripts')
    parser.set_defaults(blank_serial=False)

    args = parser.parse_args()
    
    user = args.u
    if not args.p:
        user_pass = getpass("Enter password for user {}: ".format(user))
    else:
        user_pass = args.p
    search_customer = args.search_customer
    search_string = args.search_string
    sort_order = args.sort_order
    node_id = args.node_id

    return user, user_pass, search_customer, search_string, sort_order, node_id


def get_inputs_inventory():
    """
    Get the inputs for connecting to the cluster
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='user',
                        help='AIQ username')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='AIQ password')                        
    parser.add_argument('--version', type=str,
                        required=False,
                        metavar='search_vers',
                        help='Version of Element to search on')
    parser.add_argument('--model', type=str.upper,
                        required=False,
                        metavar='search_model',
                        help='Type of node to search on')
    parser.add_argument('--search-customer', type=str.lower,
                        required=False,
                        metavar='search_customer',
                        dest='search_customer',
                        help='Customer to search on')
    parser.add_argument('--no-serial',
                        action='store_true')
    parser.set_defaults(blank_serial=False)

    args = parser.parse_args()
    
    user = args.u
    if not args.p:
        user_pass = getpass("Enter password for user {}: ".format(user))
    else:
        user_pass = args.p
    if args.version is not None:
        search_vers = args.version
    else:
        search_vers = None
    if args.model is not None:
        search_model = args.model
    else:
        search_model = None
    if args.no_serial:
        blank_serial = True
    else:
        blank_serial = False
    search_customer = args.search_customer
    return user, user_pass, search_vers, search_model, blank_serial, search_customer


def get_inputs_logs():
    """
    Get the inputs for connecting to the cluster
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='user',
                        help='AIQ username')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='AIQ password')
    parser.add_argument('--search-customer', type=str.lower,
                        required=False,
                        metavar='customer name',
                        dest='search_customer',
                        help='customer name to search on')
    parser.add_argument('--search-string', type=str.lower,
                        required=False,
                        metavar='text to search for',
                        dest='search_string',
                        help='log text to search for')
    parser.add_argument('--sort-order',
                        choices=["Cluster", "Date", "Severity", "Details", "Type"],
                        required=False,
                        metavar='sort_order',
                        dest='sort_order',
                        help='column to sort on for certain script outputs')
    parser.add_argument('--search-cluster', type=str.lower,
                        required=False,
                        metavar='search_cluster',
                        dest='search_cluster',
                        help='search for a particular cluster in an output')
    parser.set_defaults(blank_serial=False)

    args = parser.parse_args()
    
    user = args.u
    if not args.p:
        user_pass = getpass("Enter password for user {}: ".format(user))
    else:
        user_pass = args.p
    search_customer = args.search_customer
    search_string = args.search_string
    sort_order = args.sort_order
    search_cluster = args.search_cluster

    return user, user_pass, search_customer, search_string, sort_order, search_cluster


def get_inputs_disks():
    """
    Get the inputs for connecting to the cluster
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='user',
                        help='AIQ username')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='AIQ password')
    parser.add_argument('--search-customer', type=str.lower,
                        required=False,
                        metavar='customer name',
                        dest='search_customer',
                        help='customer name to search on')
    parser.add_argument('--search-cluster', type=str.lower,
                        required=False,
                        metavar='search_cluster',
                        dest='search_cluster',
                        help='search for a particular cluster in an output')
    parser.set_defaults(blank_serial=False)

    args = parser.parse_args()
    
    user = args.u
    if not args.p:
        user_pass = getpass("Enter password for user {}: ".format(user))
    else:
        user_pass = args.p
    search_customer = args.search_customer
    search_cluster = args.search_cluster

    return user, user_pass, search_customer, search_cluster


def get_inputs_suppress():
    """
    Get the inputs for connecting to the cluster
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='user',
                        help='AIQ username')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='AIQ password')
    parser.add_argument('--search-customer', type=str.lower,
                        required=False,
                        metavar='customer name',
                        dest='search_customer',
                        help='customer name to search on')
    parser.add_argument('--search-cluster', type=str.lower,
                        required=False,
                        metavar='search_cluster',
                        dest='search_cluster',
                        help='search for a particular cluster in an output')
    parser.add_argument('--duration', type=int,
                        metavar='dur_sec',
                        required=True,
                        help='Duration time in seconds, default 14400 (4hrs)')
    parser.add_argument('--suppress-type',
                        choices=['upgrade', 'full'],
                        default="full",
                        required=False,
                        metavar='suppress_type',
                        dest='suppress_type',
                        help=('Is this suppression full or for an upgrade, '
                             'default is full'))
    parser.set_defaults(blank_serial=False)

    args = parser.parse_args()
    
    user = args.u
    if not args.p:
        user_pass = getpass("Enter password for user {}: ".format(user))
    else:
        user_pass = args.p
    search_customer = args.search_customer
    search_cluster = args.search_cluster
    dur_sec = args.duration
    sup_type = args.suppress_type

    return user, user_pass, search_customer, search_cluster, dur_sec, sup_type


def main():
    """
    Nothing here as this is a module
    """
    print(f"This is a support module and has no output of its own")

if __name__ == "__main__":
    main()
