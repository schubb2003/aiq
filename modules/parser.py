#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.7 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""

def parse_cluster(parse_dict_in, search_cluster=None):
    """
    This is designed to allow someone to parse on a cluster for filtering
        outputs
    """
    parsed_dict = {}
    if search_cluster is None:
        parsed_dict = parse_dict_in
        return parsed_dict
    else:
        for key,val in parse_dict_in.items():
            if search_cluster in key.lower():
                parsed_dict[key] = val
    return parsed_dict

def main():
    """
    Nothing here as this is a module
    """
    print(f"This is a support module and has no output of its own")

if __name__ == "__main__":
    main()
