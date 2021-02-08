#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.7 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""

import sys, time, os
from datetime import datetime
from prettytable import PrettyTable
from modules.get_aiq_inputs import get_inputs_logs as get_inputs
from modules.connect_auth_aiq import web_login, build_headers, build_connect
from modules.get_aiq_customer import parse_customer
from modules.parser import parse_cluster


def build_payload():
    payload = ({"method": "ListClusterDetails",
                "params": {},
                "id": 1})
    return payload


def build_cluster_events(cls_id):
    fault_payload = ({"method": "ListClusterFaults", 
                      "params": {
                        "clusterID": cls_id
                        }, 
                      "id": 1
                    })
    return fault_payload


def build_events(headers, search_string=None, **cluster_dict):
    """
    Build the events list
    """
    flt_dict_pre = {}
    for cls_name, cls_id in cluster_dict.items():
        payload = build_cluster_events(cls_id)
        response_json = build_connect(headers, payload)
        for res_out in response_json['result']['faults']:
            if res_out['resolved']  == False:
                flt_details = res_out['details']
                flt_node = res_out['nodeID']
                flt_drive = res_out['driveID']
                flt_svc = res_out['serviceID']
                flt_date = res_out['date']
                flt_type = res_out['type']
                flt_sev = res_out['severity']
                flt_key = cls_name + "_" + str(res_out['clusterFaultID'])
                if search_string != None:
                    if search_string.lower() in (res_out['details']).lower():
                         flt_dict_pre[flt_key] = [flt_node, flt_drive, 
                                                  flt_svc, flt_date, flt_type, 
                                                  flt_sev, flt_details]
                elif search_string == None:
                    flt_dict_pre[flt_key] = [flt_node, flt_drive, 
                                             flt_svc, flt_date, flt_type, 
                                             flt_sev, flt_details]
                else:
                    pass
    if len(flt_dict_pre) == 0:
        print(f"No events found")
    return flt_dict_pre


def print_table(outfile_name, sort_order=None, **flt_dict):
    if sort_order is None:
        sort_order = "Type"
    flt_table = PrettyTable()
    flt_table.field_names = ["Cluster", "Node ID", "Drive ID", "Service ID",
                             "Date", "Type","Severity", "Details"]
    #flt_table.max_width['Details'] = 60
    for key, val in flt_dict.items():
        cls_name = key.split("_")[0]
        flt_node = val[0]
        flt_drive = val[1]
        flt_svc = val[2]
        flt_date = val[3]
        flt_type = val[4]
        flt_sev = val[5]
        flt_details = val[6]
        flt_table.add_row([cls_name, flt_node, flt_drive, flt_svc,
                           flt_date, flt_type, flt_sev, flt_details])
    print(flt_table.get_string(sortby=sort_order))
    flt_table_text = flt_table.get_string()
    with open("./output_files/" + outfile_name, "a") as out_file:
        out_file.write(flt_table_text + "\n")


def get_filename():
    """
    Build the output filename
    """
    now_date = datetime.now()
    out_date = now_date.strftime("%Y-%m-%d_%H-%M")
    outfile_name = "cluster_faults_" + out_date + '.txt'
    if os.path.exists(outfile_name):
        os.remove(outfile_name)
    print('Output file name is: {}'.format(outfile_name))
    return outfile_name


def main():
    """
    Do the work
    """
    user, user_pass, search_customer, search_string, sort_order, search_cluster  = get_inputs()
    auth_cookie = web_login(user, user_pass)
    payload = build_payload()
    headers = build_headers(auth_cookie)
    response_json = build_connect(headers, payload)
    cluster_dict = parse_customer(response_json, search_customer)
    flt_dict_pre = build_events(headers, search_string, **cluster_dict)
    flt_dict = parse_cluster(flt_dict_pre, search_cluster)
    outfile_name = get_filename()
    print_table(outfile_name, sort_order, **flt_dict)


if __name__ == "__main__":
    main()
