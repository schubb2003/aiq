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
    gb_div = 1073741824
    cap_dict_pre = {}
    for key,val in response_dict.items():
        cls_cap = val['clusterCapacity']
        cls_name = key
        used_meta_snap_space = cls_cap['usedMetadataSpaceInSnapshots']
        used_meta_snap_space_gb = round((used_meta_snap_space/gb_div),2)

        max_used_meta = cls_cap['maxUsedMetadataSpace']
        max_used_meta_gb = round((max_used_meta/gb_div),2)

        actv_space = cls_cap['activeBlockSpace']
        actv_space_gb = round((actv_space/gb_div),2)

        uniq_blck_used_space = cls_cap['uniqueBlocksUsedSpace']
        uniq_blck_used_space_gb = round((uniq_blck_used_space/gb_div),2)

        total_ops = cls_cap['totalOps']
        peak_actv_sess = cls_cap['peakActiveSessions']
        uniq_block = cls_cap['uniqueBlocks']
        max_over_prov = cls_cap['maxOverProvisionableSpace']
        max_over_prov_gb = round((max_over_prov/gb_div),2)

        zero_blocks = cls_cap['zeroBlocks']
        prov_space = cls_cap['provisionedSpace']
        prov_space_gb = round((prov_space/gb_div),2)

        max_used = cls_cap['maxUsedSpace']
        max_used_gb = round((max_used/gb_div),2)

        peak_iops = cls_cap['peakIOPS']
        time_stamp = cls_cap['timestamp']
        curr_iops = cls_cap['currentIOPS']
        used_space = cls_cap['usedSpace']
        used_space_gb = round((used_space/gb_div),2)

        actv_sess = cls_cap['activeSessions']
        non_zero_block = cls_cap['nonZeroBlocks']
        max_prov = cls_cap['maxProvisionedSpace']
        max_prov_gb = round((max_prov/gb_div),2)

        used_meta = cls_cap['usedMetadataSpace']
        used_meta_gb = round((used_meta/gb_div),2)

        avg_iops = cls_cap['averageIOPS']
        snap_non_zero_block = cls_cap['snapshotNonZeroBlocks']
        max_iops = cls_cap['maxIOPS']
        io_size = cls_cap['clusterRecentIOSize']
        cap_dict_pre[cls_name] =[time_stamp, used_meta_snap_space_gb, 
								 max_used_meta_gb, used_meta_gb,
								 uniq_blck_used_space_gb, uniq_block, 
								 zero_blocks, non_zero_block, 
								 snap_non_zero_block, max_over_prov_gb,
								 max_prov_gb, prov_space_gb, max_used_gb,
								 used_space_gb, actv_space_gb,
								 peak_actv_sess, io_size, total_ops, curr_iops, 
								 avg_iops, max_iops, peak_iops, actv_sess]
    return cap_dict_pre


def build_output(outfile_name, **cap_dict):
    out_table = PrettyTable()
    out_table.field_names = ["Cluster", "Timestamp","Used Metadata Snap Space", 
                             "Max Used Metadata", "Used Metadata",
                             "Unique block space used", "Unique blocks",
                             "Zero blocks", "Non Zero Blocks", 
                             "Snapshot Non Zero Blocks", "Max Overprovisionable",
                             "Max Provisioned", "Provisioned Space",
                             "Max Usable Space", "Used Space", "Active Space",
                             "Peak Active Sessions", "Active Sessions",
                             "Recent IO Size", "Total Ops", "Current IOPs",
                             "Average IOPs", "Maximum IOPs", "Peak IOPs"]
    for key,val in cap_dict.items():
        cls_name = key
        time_stamp = val[0]
        used_meta_snap_space_gb = val[1]
        max_used_meta_gb = val[2]
        used_meta_gb = val[3]
        uniq_blck_used_space_gb = val[4]
        uniq_block = val[5]
        zero_blocks = val[6]
        non_zero_block = val[7]
        snap_non_zero_block = val[8]
        max_over_prov_gb = val[9]
        max_prov_gb = val[10]
        prov_space_gb = val[11]
        max_used_gb = val[12]
        used_space_gb = val[13]
        actv_space_gb = val[14]
        peak_actv_sess = val[15]
        io_size = val[16]
        total_ops = val[17]
        curr_iops = val[18]
        avg_iops = val[19]
        max_iops = val[20]
        peak_iops = val[21]
        actv_sess = val[22]
        out_table.add_row([cls_name, time_stamp, used_meta_snap_space_gb, 
						   max_used_meta_gb, used_meta_gb,
						   uniq_blck_used_space_gb, uniq_block, 
						   zero_blocks, non_zero_block, 
						   snap_non_zero_block, max_over_prov_gb,
						   max_prov_gb, prov_space_gb, max_used_gb,
						   used_space_gb, actv_space_gb,
						   peak_actv_sess, io_size, total_ops, curr_iops, 
						   avg_iops, max_iops, peak_iops, actv_sess])
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
    outfile_name = "cluster_capacity_" + out_date + '.txt'
    if os.path.exists(outfile_name):
        os.remove(outfile_name)
    print('Output file name is: {}'.format(outfile_name))
    return outfile_name


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
    response_dict = build_response(headers, cluster_dict, search_string=None,
                                   api_call='GetClusterCapacity', node_id=None)
    outfile_name = get_filename(search_customer)
    cap_dict_pre = build_events(response_dict, search_string)
    cap_dict = parse_cluster(cap_dict_pre, search_cluster)
    build_output(outfile_name, **cap_dict)

if __name__ == "__main__":
    main()
