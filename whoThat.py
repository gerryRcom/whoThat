#!/usr/bin/python3
# 
import os
import re
import json
import requests
from requests.auth import HTTPBasicAuth

# Pull creds for geoip service from config file.
def getConfig():
    configContent = []
    with open('whoThat.config') as configFile:
        for line in configFile:
            configContent.append(line)
    return(configContent)

# query geolite for the IP's country and just return the country name in English
def queryLocation():
    geoCreds = getConfig()
    response = requests.get('https://geolite.info/geoip/v2.1/country/109.76.171.49?pretty',auth=HTTPBasicAuth(geoCreds[0].strip(), geoCreds[1].strip()))
    responseJson = json.loads(response.text)
    # just return the country value from the JSON content
    return(responseJson["country"]["names"]["en"])

# extract IPs from log file and tally amount of time's they feature.
with open('./logs/access.log.1') as file:
    uniqueIP = {}
    for line in file:
        ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
        # increment by one if ip is already in the dict, if it's not, add it to the dict.
        if ip[0] in uniqueIP:
            uniqueIP[ip[0]] += 1
        else:
            uniqueIP[ip[0]] = 1


    print(uniqueIP)

print(queryLocation())


