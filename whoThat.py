#!/usr/bin/python3
import os
import re
import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

# Declare constants
LOG_LOCATION="./logs/access.log.1"
STATS_LOCATION="."
STATS_LOG_LOCATION=STATS_LOCATION+"/stats/"

# Pull creds for geoip service from config file.
def getConfig():
    configContent = []
    with open('whoThat.config') as configFile:
        for line in configFile:
            configContent.append(line)
    return(configContent)

# query geolite for the IP's country and just return the country name in English
def queryLocation(ipAddress):
    geoCreds = getConfig()
    response = requests.get('https://geolite.info/geoip/v2.1/country/' + ipAddress + '?pretty',auth=HTTPBasicAuth(geoCreds[0].strip(), geoCreds[1].strip()))
    responseJson = json.loads(response.text)
    # just return the country value from the JSON content
    return(responseJson["country"]["names"]["en"])

# extract IPs from log file and tally amount of time's they feature.
def queryLog(logLocation):
    with open(logLocation) as file:
        uniqueIP = {}
        for line in file:
            ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
            # increment by one if ip is already in the dict, if it's not, add it to the dict.
            if ip[0] in uniqueIP:
                uniqueIP[ip[0]] += 1
            else:
                uniqueIP[ip[0]] = 1
    return(uniqueIP)

# generate stats htm page to embed all previous stats files and tidy up
def generateStats(statsDir):
    with open(STATS_LOCATION+"/stats.htm", 'w') as stats:
        stats.write("<html><head><title>Stats for gerryR.com</title></head><body><table>\n")
        for file in os.listdir(statsDir):
            currentFile = os.path.join(statsDir, file)
            # checking if it is a file
            if os.path.isfile(currentFile):
                stats.write("<iframe width=\"25%\" height=\"25%\" src="+currentFile+" title=\"Stats\"></iframe></br>\n")
        stats.write("</body></html>\n")

if __name__ == "__main__":
    dateStamp = datetime.today().date() - timedelta(days=1)
    logContents = queryLog(LOG_LOCATION)
    hitsPerCountry = {}
    for key, value in logContents.items():
        location = queryLocation(key)
        if location in hitsPerCountry:
            hitsPerCountry[location] += 1
        else:
            hitsPerCountry[location] = 1
    
    # generate htm page with yesterdays stats from yesterdays logs
    with open(STATS_LOG_LOCATION+str(dateStamp)+".htm", 'w') as stats:
        stats.write("<html><head><title>Stats for "+str(dateStamp)+"</title></head><body><table><tr><td>Stats for "+str(dateStamp)+"</td></tr>\n")
        for country, qty in sorted(hitsPerCountry.items()):
            stats.write("<tr><td>{0}</td><td>{1}</td></tr>\n".format(country, str(qty)))
        stats.write("</table></body></html>\n")
    generateStats("./stats")