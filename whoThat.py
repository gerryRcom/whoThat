#!/usr/bin/python3
# 
import os
import re

# Pull creds for geoip service from config file.
def getCreds():
    with open('whoThat.config') as credFile:
        for line in credFile:

            print(line.strip())

# extract IPs from log file and tally amount of time's they feature.
with open('./logs/access.log.1') as file:
    uniqueIP = {}
    for line in file:
        ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
        print(ip[0])
        if ip[0] in uniqueIP:
            uniqueIP[ip[0]] += 1
        else:
            uniqueIP[ip[0]] = 1


    print(uniqueIP)
getCreds()



    



# 