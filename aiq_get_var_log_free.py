#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.7 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""

import sys, time, os
import requests
from datetime import datetime
from prettytable import PrettyTable
from modules.get_aiq_inputs import get_inputs_logs as get_inputs
from modules.connect_auth_aiq import web_login, build_headers, build_connect
from modules.get_aiq_customer import parse_customer
from modules.build_api_response import build_response
from modules.parser import parse_cluster


def build_payload():
    payload = ({"method": "ListClusterDetails",
                "params": {},
                "id": 1})
    return payload


def build_events(response_dict, search_string):
    """
    Build the events list
    """
    constant_list = []
    constant_dict_pre = {}
    for key,val in response_dict.items():
        cluster_name = key
        response_json = val
        if search_string is not None:
            for cls_constant in search_string.split(","):
                for dict_key in response_json.keys():
                    if cls_constant in dict_key.lower():
                        constant_list.append(dict_key)
                        constant_out = response_json[dict_key]
                        cls_key = cluster_name + "_" + dict_key
                        constant_dict_pre[cls_key] = constant_out
            if len(constant_list) == 0:
                print(f"\t{cls_constant} not found")
                sys.exit(1)
        elif search_string is None:
            for dict_key in response_json.keys():
                    constant_out = response_json[dict_key]
                    cls_key = cluster_name + "-" + dict_key
                    constant_dict_pre[cls_key] = constant_out
        else:
            sys.exit(1)
    return constant_dict_pre


def build_output(outfile_name, **constant_dict):
    out_table = PrettyTable()
    out_table.field_names = ["Cluster","Constant Name", "Constant Setting"]
    #out_table.max_width['Constant Setting'] = 60
    out_table.align["Constant Name"] = "l"
    out_table.align["Constant Setting"] = "l"
    for key,val in constant_dict.items():
        cls_name = key.split("-")[0]
        cnst_name = key.split("-")[1]
        cnst_out = val
        out_table.add_row([cls_name, cnst_name, cnst_out])
    out_table_text = out_table.get_string()
    print(out_table)
    with open("./output_files/" + outfile_name, "a") as out_file:
        out_file.write(out_table_text + "\n")   


def get_filename(cluster_name):
    """
    Build the output filename
    """
    now_date = datetime.now()
    out_date = now_date.strftime("%Y-%m-%d_%H-%M")
    outfile_name = "cluster_constants_" + out_date + '.txt'
    if os.path.exists(outfile_name):
        os.remove(outfile_name)
    print('Output file name is: {}'.format(outfile_name))
    return outfile_name


def parse_response(response_dict):
    for fs_key, fs_val in response_dict.items():
        print(36*"#")
        print(f"Cluster:\t{fs_key}")
        print(36*"#")
        hdr1 = "Node ID"
        hdr2 = "Size"
        hdr3 = "Available"
        hdr4 = "Free"
        hdr5 = "Percent Free"
        print(f"{hdr1:>11}{hdr2:>11}{hdr3:>11}{hdr4:>11}{hdr5:>14}")
        for nodes in fs_val['nodes']:
            #print(nodes)
            node_id = nodes['nodeID']
            for mount_entry in nodes['result']['mountEntries']:
                if mount_entry['directory'] == '/var/log':
                    fs_size = round((mount_entry['capacity']/1024/1024/1024),2)
                    fs_avail = round((mount_entry['available']/1024/1024/1024),2)
                    fs_free = round((mount_entry['free']/1024/1024/1024),2)
                    pct_free = round((fs_free/fs_size*100),2)
                    print(f"{node_id:>11}{fs_size:>10}G{fs_avail:>10}G"
                          f"{fs_free:>10}G{pct_free:>13}%\n")

def main():
    """
    Do the work
    """
    user, user_pass, search_customer, search_string, _sort_by, search_cluster = get_inputs()
    auth_cookie = web_login(user, user_pass)
    payload = build_payload()
    headers = build_headers(auth_cookie)
    response_json = build_connect(headers,payload)
    cluster_dict = parse_customer(response_json, search_customer)
    response_dict = build_response(headers, cluster_dict, search_string, api_call='ListMountedFileSystems', node_id=None)
    #print(response_dict)
    parse_response(response_dict)
    #outfile_name = get_filename(search_customer)
    #constant_dict_pre = build_events(response_dict, search_string)
    #constant_dict = parse_cluster(constant_dict_pre, search_cluster)
    #build_output(outfile_name, **constant_dict)

if __name__ == "__main__":
    main()
