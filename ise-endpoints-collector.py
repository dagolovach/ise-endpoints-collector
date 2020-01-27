#!/usr/bin/env python3

"""
Script to collect MAC addresses of endpoints in old and new ISE deployments for the migration purposes and comparison/

Idea:
    - Predefined and equal Group in both ISE clusters
    - API to old ISE, check groups, collect endpoints from those groups and keep them in the file - ise_groups_old.json
    - API to new ISE, check groups, collect endpoints from those groups and keep them in the file - ise_groups_new.json
    - Compare ise_groups_old.json and ise_groups_new.json

Files:
    ise-endpoints-collector.py - main script
    ise_groups_old.json - file to collect groups and MAC addresses from old ISE
    ise_groups_new.json - file to collect groups and MAC addresses from old ISE

"""

# Imports
import time
import requests
import json
from requests.auth import HTTPBasicAuth

# Disable warnings(InsecureRequestWarning) because of the certificate
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Module "Global" Variables
ise_groups = [
    "GROUP_A",
    "GROUP_B",
    "GROUP_C",
]

ise_groups_url = []
ise_groups_dict = {}
dict_result = {}
mac_addresses = {}
ise_servers = {
    'ise_url': ["https://<ISE#1_PAN_IP_ADDRESS>/ers/config/", "https://<ISE#1_PAN_IP_ADDRESS>/ers/config/"],
    'header': [{'Accept': 'application/json', 'username': 'ISE#1_ERS_ADMIN_USER', 'password': 'ISE#1_ERS_ADMIN_PWD'},
               {'Accept': 'application/json', 'username': 'ISE#2_ERS_ADMIN_USER', 'password': 'ISE#2_ERS_ADMIN_PWD'}],
    'destination': ['ise_groups_old.json', 'ise_groups_new.json']
}


# Module Functions and Classes
def get_group_id(ise_groups, ise_url, header):
    """
    Get group id from the group name
    :param ise_groups: list of ISE groups
    :param ise_url: list of ISE urls
    :param header: dictionary with GET header (Accept and Auth)
    :return: ise_groups_dict dictionary with {group_name: group_ids}
    """
    for each in ise_groups:
        url = ise_url + "endpointgroup?filter=name.EQ." + each
        headers = header
        user = header['username']
        password = header['password']
        payload = {}
        response = requests.request("GET", url, auth=HTTPBasicAuth(user, password), headers=headers, data=payload, verify=False)
        data = response.json()
        ise_groups_url.append(data['SearchResult']['resources'][0]['id'])
        ise_groups_dict[each] = data['SearchResult']['resources'][0]['id']

    return ise_groups_dict


def get_mac_addresses(ise_groups_url, ise_url, header):
    """
    Collect MAC addresses from the provided groups
    :param ise_groups_url: list of ISE groups
    :param ise_url: list of ISE urls
    :param header: dictionary with GET header (Accept and Auth)
    :return: mac_addresses dictionary with MAC addresses per group {group_name: list[MAC addresses]}
    """
    for key, value in ise_groups_url.items():
        mac_addresses[key] = []
        url = ise_url + "endpoint?filter=groupId.EQ." + str(value)
        headers = header
        payload = {}
        user = header['username']
        password = header['password']
        while True:
            response = requests.request("GET", url, auth=HTTPBasicAuth(user, password), headers=headers, data=payload, verify=False)
            data = response.json()
            for each in data['SearchResult']['resources']:
                mac_addresses[key].append(each['name'])

            if 'nextPage' in data['SearchResult']:
                url = data['SearchResult']['nextPage']['href']
                continue
            else:
                break
    return mac_addresses


def search_mac_address(search_mac, dict_result):
    """
    In progress, not finished yet
    :param search_mac:
    :param dict_result:
    :return:
    """
    for group, mac in dict_result.items():
        if search_mac in mac:
            print(group)
            break
    return

def compare_groups():
    """
    Compare ise_groups_new.json and ise_groups_old.json
    :return: Print difference
    """
    new_file = open('ise_groups_new.json', 'r')
    old_file = open('ise_groups_old.json', 'r')

    new_file_dict = json.load(new_file)
    old_file_dict = json.load(old_file)
    for key, value in old_file_dict.items():
        for each in value:
            if each in new_file_dict[key]:
                continue
            else:
                print(f'{each} - Found in Old ISE#1 but not in New ISE#2')

    print('---' * 10)

    for key, value in new_file_dict.items():
        for each in value:
            if each in old_file_dict[key]:
                continue
            else:
                print(f'{each} - Found in New ISE#2 but not in Old ISE#1')

    new_file.close()
    old_file.close()
    pass


def main():
    """
    Main function, collect group_id from group name, and collect MAC addresses per group
    :return: nothing
    """
    for i in range(len(ise_servers['ise_url'])):
        ise_url = ise_servers['ise_url'][i]
        header = ise_servers['header'][i]
        destination = ise_servers['destination'][i]
        ise_groups_url = get_group_id(ise_groups, ise_url, header)
        dict_result = get_mac_addresses(ise_groups_url, ise_url, header)
        # for key, value in dict_result.items():
        #    print(f"Group {key} has {len(value)} endpoints")
        with open(destination, 'w') as f:
            json.dump(dict_result, f, indent=2)

    compare_groups()


# Check to see if this file is the "__main__" script being executed
if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f'{time.time() - start_time}')


