# ISE Endpoints collector
> Script to collect MAC addresses of endpoints in old and new ISE deployments for the migration purposes and comparison/

Idea:
* Predefined and equal groups in both ISE clusters
* API to old ISE, check groups, collect endpoints from those groups and keep them in the file - ise_groups_old.json
* API to new ISE, check groups, collect endpoints from those groups and keep them in the file - ise_groups_new.json
* Compare ise_groups_old.json and ise_groups_new.json

Files:
* ise-endpoints-collector.py - main script
* ise_groups_old.json - file to collect groups and MAC addresses from old ISE
* ise_groups_new.json - file to collect groups and MAC addresses from old ISE

Changes before use:
* ise_groups = [] list
* ISE#1_PAN_IP_ADDRESS
* ISE#1_ERS_ADMIN_USER
* ISE#1_ERS_ADMIN_PWD
* ISE#2_PAN_IP_ADDRESS
* ISE#2_ERS_ADMIN_USER
* ISE#2_ERS_ADMIN_PWD

## Technologies
* Python3
* Cisco ISE

## Setup
* Breakdown post [here](https://dmitrygolovach.com/python-and-cisco-ise-collect-endpoints/)
* How it works [youtube](https://youtu.be/RK-ydhJAO-4)

## Contact
* Created by Dmitry Golovach
* Web: [https://dagolovachgolovach.com](https://dmitrygolovach.com) 
* Twitter: [@dagolovach](https://twitter.com/dagolovach)
* LinkedIn: [@dmitrygolovach](https://www.linkedin.com/in/dmitrygolovach/)

- feel free to contact me!