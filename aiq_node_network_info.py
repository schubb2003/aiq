#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.7 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
# This script gets the network config from a single node for a node replacment
#
# Example output
"""

import sys, os
from datetime import datetime
from prettytable import PrettyTable
from modules.get_aiq_inputs import get_inputs
from modules.connect_auth_aiq import web_login, build_headers, build_connect
from modules.get_aiq_customer import parse_customer
from modules.build_api_response import build_response

def build_payload():
    payload = ({"method": "ListClusterDetails",
                "params": {},
                "id": 1})
    return payload


def build_network(response_dict, node_id,search_string):
    """
    Get the bond configs and call the function to build the output
    """
    node_out = {}
    netBonds = ["Bond1G", "Bond10G"]
    for key,val in response_dict.items():
        if key.lower() == search_string:
            for node in val['nodes']:
                for bond in netBonds:
                    if node['nodeID'] == node_id:
                        addr = (node['result']['network']
                                [bond]['address'])
                        bond_mode = (node['result']['network']
                                    [bond]['bond-mode'])
                        dns_search = (node['result']['network']
                                    [bond]['dns-search'])
                        dns_servers = (node['result']['network']
                                    [bond]['dns-nameservers'])
                        mtu = (node['result']['network']
                            [bond]['mtu'])
                        mask = (node['result']['network']
                                [bond]['physical']['netmask'])
                        gateway = (node['result']['network']
                                [bond]['gateway'])
                        vlan = (node['result']['network']
                                [bond]['virtualNetworkTag'])
                        node_out[bond] = [addr, bond_mode, dns_search, 
                                          dns_servers, mtu, mask, gateway, vlan]
    if node_out is not None:
        return node_out
    else:
        print(f"No matching node found")
        sys.exit(1)

def build_output(outfile_name, node_out):
    out_table = PrettyTable()
    out_table.field_names = ["Bond", "Address", "Mode", "DNS Search",
                             "DNS servers", "MTU", "Netmask", "Gateway", "VLAN"]
    for bond,vals in node_out.items():
        out_table.add_row([bond, vals[0],vals[1],vals[2],
                          vals[3], vals[4], vals[5], vals[6], vals[7]])
    out_table_text = out_table.get_string()
    print(out_table)
    with open("./output_files/" + outfile_name, "a") as out_file:
        out_file.write(out_table_text + "\n")   


def get_filename():
    """
    Build the output filename
    """
    now_date = datetime.now()
    out_date = now_date.strftime("%Y-%m-%d_%H-%M")
    outfile_name = "node_ip_cfg_info_" + out_date + '.txt'
    if os.path.exists(outfile_name):
        os.remove(outfile_name)
    print('Output file name is: {}'.format(outfile_name))
    return outfile_name


def main():
    """
    Call the functions from above
    """
    user, user_pass, search_customer, search_string, _sort_by, node_id = get_inputs()
    auth_cookie = web_login(user, user_pass)
    payload = build_payload()
    headers = build_headers(auth_cookie)
    response_json = build_connect(headers,payload)
    cluster_dict = parse_customer(response_json, search_customer)
    response_dict = build_response(headers, cluster_dict, search_string, api_call='GetNetworkConfig', node_id=node_id)
    node_out = build_network(response_dict, node_id, search_string)
    outfile_name = get_filename()
    build_output(outfile_name, node_out)

if __name__ == "__main__":
    main()
