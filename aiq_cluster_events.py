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
    event_payload = ({"method": "ListEvents", 
                      "params": {
                        "clusterID": cls_id
                        }, 
                      "id": 1
                    })
    return event_payload


def build_events(headers, search_string=None, **cluster_dict):
    """
    Build the events list
    """
    evt_dict_pre = {}
    for cls_name, cls_id in cluster_dict.items():
        payload = build_cluster_events(cls_id)
        response_json = build_connect(headers, payload)
        evt_out = response_json['result']['events']
        for event in evt_out:
            evt_id_str = str(event['eventID'])
            cls_evt = cls_name + "_" + evt_id_str
            node_id = event['nodeID']
            drive_id = event['driveID']
            svc_id = event['serviceID']
            evt_message = event['message']
            evt_type = event['eventInfoType']
            evt_sev = event['severity']
            evt_details = event['details']
            evt_aiq_time = event['timeOfPublish']
            evt_time = event['timeOfReport']
            if search_string is not None:
                if search_string in evt_type.lower():
                    evt_type = evt_type
                    evt_dict_pre[cls_evt] = [node_id, drive_id, svc_id,
                                            evt_type, evt_message, evt_sev, 
                                            evt_details, evt_aiq_time, evt_time]
            elif search_string is None:
                evt_dict_pre[cls_evt] = [node_id, drive_id, svc_id,
                                        evt_type, evt_message, evt_sev, 
                                        evt_details, evt_aiq_time, evt_time]            

    if len(evt_dict_pre) == 0:
        print(f"No events found")
        sys.exit(1)
    return evt_dict_pre


def print_table(outfile_name, sort_order=None, **evt_dict_pre):
    sort_order = "Type"
    evt_table = PrettyTable()
    evt_table.field_names = ["Cluster", "Event ID", "Node ID", "Drive ID",
                             "Service ID", "Type", "Message", "Severity",
                             "Details", "Report to AIQ Time", "Event Time"]
    #evt_table.max_width['Details'] = 60
    #evt_table.max_width['Message'] = 60
    for key, val in evt_dict_pre.items():
        cls_name = key.split("_")[0]
        evt_id = key.split("_")[1]
        evt_node_id = val[0]
        evt_drive_id = val[1]
        evt_svc_id = val[2]
        evt_type = val[3]
        evt_message = val[4]
        evt_sev = val[5]
        evt_details = val[6]
        evt_aiq_time = val[7]
        evt_time = val[8]
        evt_table.add_row([cls_name, evt_id, evt_node_id, evt_drive_id,
                           evt_svc_id, evt_type, evt_message, evt_sev,
                           evt_details, evt_aiq_time, evt_time])
    print(evt_table)
    evt_table_text = evt_table.get_string()
    with open("./output_files/" + outfile_name, "a") as out_file:
        out_file.write(evt_table_text + "\n")


def get_filename():
    """
    Build the output filename
    """
    now_date = datetime.now()
    out_date = now_date.strftime("%Y-%m-%d_%H-%M")
    outfile_name = "cluster_events_" + out_date + '.txt'
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
    evt_dict_pre = build_events(headers, search_string, **cluster_dict)
    evt_dict = parse_cluster(evt_dict_pre, search_cluster)
    outfile_name = get_filename()
    print_table(outfile_name, sort_order, **evt_dict)


if __name__ == "__main__":
    main()
