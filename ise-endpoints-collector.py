#!/usr/bin/env python3

"""
doc-string
"""

# Imports
import time
import requests
import json

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
    'ise_url': ["https://3.45.48.12:9060/ers/config/", "https://3.45.48.24:9060/ers/config/"],
    'header': [{'Accept': 'application/json', 'Authorization': 'Basic YWRtaW46VjByMHRuMWs=', },
               {'Accept': 'application/json', 'Authorization': 'Basic Y2lzY286VjByMHRuMWs=', }],
    'destination': ['ise_groups_old.json', 'ise_groups_new.json']
}


# Module Functions and Classes
def get_group_id(ise_groups, ise_url, header):
    for each in ise_groups:
        url = ise_url + "endpointgroup?filter=name.EQ." + each
        headers = header
        payload = {}
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        data = response.json()
        ise_groups_url.append(data['SearchResult']['resources'][0]['id'])
        ise_groups_dict[each] = data['SearchResult']['resources'][0]['id']

    return ise_groups_dict


def get_mac_addresses(ise_groups_url, ise_url, header):
    for key, value in ise_groups_url.items():
        mac_addresses[key] = []
        url = ise_url + "endpoint?filter=groupId.EQ." + str(value)
        headers = header
        payload = {}

        while True:
            response = requests.request("GET", url, headers=headers, data=payload, verify=False)
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
    for group, mac in dict_result.items():
        if search_mac in mac:
            print(group)
            break
    return


def main():
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
        # search_mac_address("C0:3F:D5:6F:87:EF", dict_result)


# Check to see if this file is the "__main__" script being executed
if __name__ == "__main__":
    start_time = time.time()
    main()
    print(time.time() - start_time)

    new_file = open('ise_groups_new.json', 'r')
    old_file = open('ise_groups_old.json', 'r')

    new_file_dict = json.load(new_file)
    old_file_dict = json.load(old_file)
    for key, value in old_file_dict.items():
        for each in value:
            if each in new_file_dict[key]:
                continue
            else:
                print(f'{each} - Old not in New')

    print('---' * 10)

    for key, value in new_file_dict.items():
        for each in value:
            if each in old_file_dict[key]:
                continue
            else:
                print(f'{each} - New not in OLd')

    new_file.close()
    old_file.close()
