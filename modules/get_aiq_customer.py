#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.7 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""

import sys

def parse_customer(response_json, search_customer):
    cluster_dict = {}
    cls_res = response_json['result']['clusters']
    for cluster in cls_res:
        custName = cluster['sapCompanyName']
        custName = custName.lower()
        if search_customer is not None:
            if search_customer in custName:
                #print(f"customer:\t{custName}\nSearch:\t{search_customer}")
                cls_id = cluster['id']
                cls_name = cluster['name']
                cluster_dict[cls_name] = cls_id
            else:
                pass
        elif search_customer == None:
            for cluster in cls_res:
                cls_id = cluster['id']
                cls_name = cluster['name']
                cluster_dict[cls_name] = cls_id
        else:
            pass
    return cluster_dict

def main():
    """
    Nothing here as this is a module
    """
    print(f"This is a support module and has no output of its own")

if __name__ == "__main__":
    main()
