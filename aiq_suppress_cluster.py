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
from modules.get_aiq_inputs import get_inputs_suppress as get_inputs
from modules.connect_auth_aiq import web_login, build_headers, build_connect
from modules.get_aiq_customer import parse_customer
from modules.aiq_build_api_payload import suppress_cluster_payload
from modules.parser import parse_cluster


def build_payload():
    payload = ({"method": "ListClusterDetails",
                "params": {},
                "id": 1})
    return payload


def build_output(outfile_name, **constant_dict):
    out_table = PrettyTable()
    out_table.field_names = ["Cluster","Constant Name", "Constant Setting"]
    #out_table.max_width['Constant Setting'] = 60
    for key,val in constant_dict.items():
        cls_name = key.split("_")[0]
        cnst_name = key.split("_")[1]
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
    outfile_name = "cluster_suppress_" + out_date + '.txt'
    if os.path.exists(outfile_name):
        os.remove(outfile_name)
    print('Output file name is: {}'.format(outfile_name))
    return outfile_name


def get_cluster(cluster_dict):
    for _key, val in cluster_dict.items():
        cls_id = val
    return cls_id

def main():
    """
    Do the work
    """
    user, user_pass, search_customer, search_cluster, dur_sec, sup_type = get_inputs()
    auth_cookie = web_login(user, user_pass)
    payload = build_payload()
    headers = build_headers(auth_cookie)
    response_json = build_connect(headers,payload)
    cluster_dict_pre = parse_customer(response_json, search_customer)
    cluster_dict = parse_cluster(cluster_dict_pre, search_cluster)
    cls_id = get_cluster(cluster_dict)
    suppress_payload = suppress_cluster_payload(sup_type, cls_id, dur_sec)
    response_json = build_connect(headers, suppress_payload)
    print(response_json)

if __name__ == "__main__":
    main()
