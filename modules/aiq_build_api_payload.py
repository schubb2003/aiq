#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.7 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""

def list_cluster_details_payload():
    payload = ({"method": "ListClusterDetails",
                "params": {},
                "id": 1})
    return payload


def list_active_nodes_payload(cls_id):
    payload = ({"method": "ListActiveNodes",
                "params": {
                    "clusterID": cls_id
                    },
                "id": 1})
    return payload

def get_cluster_info_payload(cls_id):
    payload = ({"method": "GetClusterInfo",
                "params": {
                    "clusterID": cls_id
                    },
                "id": 1})
    return payload

def main():
    """
    Nothing here as this is a module
    """
    print(f"This is a support module and has no output of its own")

if __name__ == "__main__":
    main()