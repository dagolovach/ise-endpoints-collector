#!/usr/bin/env python3

import json

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

print('---'*10)

for key, value in new_file_dict.items():
    for each in value:
        if each in old_file_dict[key]:
           continue
        else:
            print(f'{each} - New not in OLd')