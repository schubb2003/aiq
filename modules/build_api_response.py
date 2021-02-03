#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.7 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""

import requests

def build_response(headers, cluster_dict, search_string, api_call, node_id):
    """
    Connect to AIQ to get the data
    """
    response_dict = {}
    cluster_vals = cluster_dict.values()
    for cls_id in cluster_vals:
        str_cls_id = str(cls_id)
        url = "https://activeiq.solidfire.com/state/cluster/" + str_cls_id + "/" + api_call
        response = requests.get(url=url, headers=headers)
        res_code = (response.status_code)
        if res_code == 404:
            print(f"{cls_id} not found")
        else:
            response_json = response.json()
            url = "https://activeiq.solidfire.com/state/cluster/" + str_cls_id + "/GetClusterInfo"
            response_cluster = requests.get(url=url, headers=headers)
            cluster_json = response_cluster.json()
            cluster_name = cluster_json['clusterInfo']['name']
            response_dict[cluster_name] = response_json
    return response_dict


def get_cluster_info(headers, cls_id):
    str_cls_id = str(cls_id)
    url = "https://activeiq.solidfire.com/state/cluster/" + str_cls_id + "/GetClusterInfo"
    response_cluster = requests.get(url=url, headers=headers)
    if response_cluster.status_code == 200:
        cluster_json = response_cluster.json()
        cluster_svip = cluster_json['clusterInfo']['svip']
        cluster_mvip = cluster_json['clusterInfo']['mvip']
    elif response_cluster.status_code == 404:
        print(f"Unable to pull from {cls_id},\n{response_cluster.text}")
        cluster_svip = "No data found"
        cluster_mvip = "No data found"
    return cluster_svip, cluster_mvip
        
def main():
    """
    Nothing here as this is a module
    """
    print(f"This is a support module and has no output of its own")

if __name__ == "__main__":
    main()
