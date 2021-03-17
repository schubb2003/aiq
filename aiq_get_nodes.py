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
from modules.get_aiq_inputs import get_inputs_inventory as get_inputs
from modules.connect_auth_aiq import web_login, build_headers, build_connect
from modules.get_aiq_customer import parse_customer
from modules.aiq_build_api_payload import list_active_nodes_payload
from modules.aiq_build_api_payload import list_cluster_details_payload
from modules.build_api_response import get_cluster_info


def get_nodes(headers, **cluster_dict):
    node_dict = {}
    node_details = []
    for cls_name, cls_id in cluster_dict.items():
        payload = list_active_nodes_payload(cls_id)
        nodes_json = build_connect(headers, payload)
        cls_svip, cls_mvip = get_cluster_info(headers, cls_id)
        node_res = nodes_json['result']['nodes']
        for node in node_res:
            node_id = node['nodeID']
            node_name = node['name']
            elem_vers = node['softwareVersion']
            node_serial = node['serialNumber']
            node_stag = node['serviceTag']
            node_type = node['nodeType']
            node_mip = node['mip']
            node_sip = node['sip']
            node_details = [cls_name, node_type, node_id, elem_vers,
                            node_serial, node_stag, node_mip, node_sip,
                            cls_mvip, cls_svip]
            node_dict[node_name] = node_details
    return node_dict


def parse_node_info(blank_serial, search_vers=None,
                    search_model=None, **node_dict):
    if search_model is not None:
        if "-" in search_model:
            search_model_series = search_model.split("-")[0]
            search_model_size = str(search_model.split("-")[1])
            search_model = search_model_series + str(search_model_size)
    node_parsed_dict = {}
    for node_name, node_details in node_dict.items():
        node_type = node_details[1]
        elem_vers = node_details[3]
        serial_num = node_details[4]
        str_evers = str(elem_vers)
        str_svers = str(search_vers)
        if "-" in node_type:
            node_type2 = node_type.split("-")[0] + str(node_type.split("-")[1])
        else:
            node_type2 = node_type
        if blank_serial == True:
            if serial_num is None:
                node_parsed_dict[node_name] = node_details
        else:
            if search_vers is not None and str(search_vers) in str(elem_vers):
                if search_model is None:
                    node_parsed_dict[node_name] = node_details
                elif search_model is not None and (search_model == node_type or
                                                   search_model == node_type2):
                    node_parsed_dict[node_name] = node_details
            elif search_model and (search_model == node_type or
                                   search_model == node_type2):
                if search_vers is None:
                    node_parsed_dict[node_name] = node_details
                elif search_vers is not None:
                    if str_svers in str_evers:
                        node_parsed_dict[node_name] = node_details
            elif search_vers is None:
                if search_model is None:
                    node_parsed_dict = node_dict
            else:
                pass

    return node_parsed_dict


def get_filename(blank_serial, search_vers=None, search_model=None):
    """
    Build the output filename
    """
    if blank_serial == True:
        search_out = "missing_serials_"
    elif search_vers is not None and search_model is None:
        search_out = "version_" + search_vers + "_"
    elif search_vers is None and search_model is not None:
        search_out = "model_" + search_model + "_"
    else:
        search_out = "full_report_"
    now_date = datetime.now()
    out_date = now_date.strftime("%Y-%m-%d_%H-%M")
    outfile_name = search_out + out_date + '.txt'
    if os.path.exists(outfile_name):
        os.remove(outfile_name)
    print('Output file name is: {}'.format(outfile_name))
    return outfile_name


def build_table(outfile_name, node_parsed_dict):
    out_table = PrettyTable()
    for node_name, node_details in node_parsed_dict.items():
        cls_name = node_details[0]
        node_type = node_details[1]
        node_id = node_details[2]
        elem_vers = node_details[3]
        node_serial = node_details[4]
        node_stag = node_details[5]
        node_mip = node_details[6]
        node_sip = node_details[7]
        cls_mvip = node_details[8]
        cls_svip = node_details[9]
        out_table.field_names = ["Cluster","Node Name", "Node ID", 
                                 "Element Vers","Node Type", "Serial No",
                                 "Service Tag", "MIP","SIP", "MVIP", "SVIP"]
        out_table.add_row([cls_name, node_name, node_id, elem_vers, node_type,
                        node_serial, node_stag, node_mip, node_sip,
                        cls_mvip, cls_svip])
    out_table_text = out_table.get_string()
    print(out_table)
    with open("./output_files/" + outfile_name, "a") as out_file:
        out_file.write(out_table_text + "\n")


def main():
    """
    Do the work
    """
    user, user_pass, search_vers, search_model, blank_serial, search_customer = get_inputs()
    payload = list_cluster_details_payload()
    auth_cookie = web_login(user, user_pass)
    headers = build_headers(auth_cookie)
    response_json = build_connect(headers, payload)
    cluster_dict = parse_customer(response_json, search_customer)
    node_dict = get_nodes(headers, **cluster_dict)
    node_parsed_dict = parse_node_info(blank_serial, search_vers,
                                       search_model, **node_dict)
    outfile_name = get_filename(blank_serial, search_vers, search_model)
    build_table(outfile_name, node_parsed_dict)

if __name__ == "__main__":
    main()
