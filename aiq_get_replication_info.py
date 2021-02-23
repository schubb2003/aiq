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

import sys
import os
from prettytable import PrettyTable
from datetime import datetime
from modules.get_aiq_inputs import get_inputs
from modules.connect_auth_aiq import web_login, build_headers, build_connect
from modules.get_aiq_customer import parse_customer
from modules.build_api_response import build_response
from modules.build_table import autosized_table_one_row as build_table

def build_payload():
    payload = ({"method": "ListClusterDetails",
                "params": {},
                "id": 1})
    return payload


def build_repl_info(response_dict, search_string):
    """
    Get the replication info for a customer
    """
    if response_dict is not None:
        repl_dict = {}
        for pair_key,pair_val in response_dict.items():
            async_count = 0
            sync_count = 0
            snap_count = 0
            if pair_key is not None and pair_val is not None:
                for vol in pair_val['volumes']:
                    vol_name = vol['name']
                    vol_id = vol['volumeID']
                    uber_key = pair_key + "_" + vol_name + "_" + str(vol_id)
                    for remote_vol in vol['volumePairs']:
                        rem_rep = remote_vol['remoteReplication']
                        rem_name = remote_vol['remoteVolumeName']
                        rem_id = remote_vol['remoteVolumeID']
                        rem_state = rem_rep['state']
                        rem_mode = rem_rep['mode']
                        repl_dict[uber_key] = [pair_key, vol_name, vol_id, 
                                               rem_name, rem_id, rem_state,
                                               rem_mode]
                        if rem_mode == "Sync":
                            sync_count = sync_count + 1
                        elif rem_mode == "Async":
                            async_count = async_count + 1
                        else:
                            snap_count = snap_count + 1
            if sync_count != 0 or async_count != 0 or snap_count != 0:
                print(f"Cluster:{pair_key}, Async:\t{async_count}, "
                    f"Sync:\t{sync_count}, Snapshot:\t{snap_count}")
        tbl_headers = ["Cluster", "Volume", "Volume ID", "Remote Vol Name",
                       "Remote Vol ID", "Remote State", "Remote mode"]
    else:
        pass
    return tbl_headers, repl_dict


def build_output(tbl_headers, repl_dict, outfile_name):
    out_tbl = PrettyTable()
    out_tbl.field_names = (tbl_headers)
    for vals in repl_dict.values():
        out_tbl.add_row([*vals])
    print(out_tbl)
    out_tbl_text = out_tbl.get_string()
    with open("./output_files/" + outfile_name, "a") as out_file:
        out_file.write(out_tbl_text + "\n")


def get_filename():
    """
    Build the output filename
    """
    now_date = datetime.now()
    out_date = now_date.strftime("%Y-%m-%d_%H-%M")
    outfile_name = "repl_info_" + out_date + '.txt'
    if os.path.exists(outfile_name):
        os.remove(outfile_name)
    print('Output file name is: {}'.format(outfile_name))
    return outfile_name


def main():
    """
    Call the functions from above
    """
    user, user_pass, search_customer, search_string, _sort_by, _node_id = get_inputs()
    auth_cookie = web_login(user, user_pass)
    payload = build_payload()
    headers = build_headers(auth_cookie)
    response_json = build_connect(headers,payload)
    cluster_dict = parse_customer(response_json, search_customer)
    response_dict = build_response(headers, cluster_dict, search_string,
                                   api_call='ListActivePairedVolumes')
    tbl_headers, repl_dict = build_repl_info(response_dict, search_string)
    outfile_name = get_filename()
    build_output(tbl_headers, repl_dict, outfile_name)

if __name__ == "__main__":
    main()
