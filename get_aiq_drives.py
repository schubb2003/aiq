#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.4 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""

import json
import os
import sys
import argparse
import requests
import time
import operator
from datetime import datetime
from getpass import getpass
from selenium import webdriver
from prettytable import PrettyTable
from modules.get_aiq_inputs import get_inputs_disks as get_inputs
from modules.connect_auth_aiq import web_login, build_connect, build_headers
from modules.get_aiq_customer import parse_customer
from modules.parser import parse_cluster


def build_payload():
    payload = ({"method": "ListClusterDetails",
                "params": {},
                 "id": 1})
    return payload


def build_response(headers, cluster_dict, filename):
    """
    Connect to AIQ to get the data
    """
    for cluster_name, cls_id in cluster_dict.items():
        str_cls_id = str(cls_id)
        url = "https://activeiq.solidfire.com/state/cluster/" + str_cls_id + "/ListDrives"
        response = requests.get(url=url, headers=headers)
        response_json = json.loads(response.text)
        build_drives(response_json, cluster_name, filename)
    #return response_json, cluster_name


def build_drives(response_json, cluster_name, filename):
    """
    Build the drive list
    """
    drive_dict = {}
    for drive_out in response_json['drives']:
        drive_serial = drive_out['serial']
        node_id = str(drive_out['nodeID'])
        node_slot = str(drive_out['chassisSlot'])
        drive_id = str(drive_out['driveID'])
        drive_dict[drive_serial] = [node_id, node_slot, drive_id, cluster_name]
    print_table(filename, drive_dict)
    #return drive_dict_pre


def get_filename(cluster_name=None):
    """
    Build the output filename
    """
    if cluster_name is None:
        cluster_name = "all_"
    now_date = datetime.now()
    out_date = now_date.strftime("%Y-%m-%d_%H-%M")
    outfile_name = "drive_info_" +cluster_name + out_date + '.txt'
    if os.path.exists(outfile_name):
        os.remove(outfile_name)
    print('Output file name is: {}'.format(outfile_name))
    return outfile_name


def print_table(outfile_name, drive_dict):
    drive_tbl = PrettyTable()
    drive_tbl.field_names = ["Cluster", "Serial Number", "Drive ID", 
                             "Node ID", "Slot Number"]
    #drive_tbl.max_width['Details'] = 60
    for key, val in drive_dict.items():
        serial_num = key
        node_id = val[0]
        node_slot = val[1]
        drive_id = val[2]
        cluster_name = val[3]
        drive_tbl.add_row([cluster_name, serial_num,
                           drive_id, node_id, node_slot])
    print(drive_tbl.get_string(sort_key=operator.itemgetter(4,5),
                               sortby="Node ID"))
    drive_tbl_text = drive_tbl.get_string(sort_key=operator.itemgetter(4,5),
                                          sortby="Node ID")
    with open("./output_files/" + outfile_name, "a") as out_file:
        out_file.write(drive_tbl_text + "\n")


def main():
    """
    Do the work
    """
    user, user_pass,search_customer, search_cluster = get_inputs()
    auth_cookie = web_login(user, user_pass)
    payload = build_payload()
    headers = build_headers(auth_cookie)
    response_json = build_connect(headers,payload)
    cluster_dict = parse_customer(response_json, search_customer)
    cluster_dict_out = parse_cluster(cluster_dict, search_cluster)
    filename = get_filename()
    build_response(headers, cluster_dict_out, filename)


if __name__ == "__main__":
    main()
