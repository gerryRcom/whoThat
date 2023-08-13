#!/usr/bin/python3
import os
import sys
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
    if os.path.isfile('whoThat.config'):
        with open('whoThat.config') as configFile:
            for line in configFile:
                configContent.append(line)
        return(configContent)
    else:
        sys.exit(1)

# query geolite for the IP's country and just return the country name in English
def queryLocation(ipAddress):
    geoCreds = getConfig()
    response = requests.get('https://geolite.info/geoip/v2.1/country/' + ipAddress + '?pretty',auth=HTTPBasicAuth(geoCreds[0].strip(), geoCreds[1].strip()))
    responseJson = json.loads(response.text)
    # just return the country value from the JSON content
    return(responseJson["country"]["names"]["en"])

# extract IPs from log file and tally amount of time's they feature.
def queryLog(logLocation):
    if os.path.isfile(logLocation):
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
    else:
        sys.exit(1)

# generate stats htm page to embed all previous stats files and tidy up
def generateStats(statsDir):
    finalData = {}
    with open(STATS_LOCATION+"/stats.htm", 'w') as stats:
        stats.write("<html><head><title>Stats for gerryR.com</title></head><body><table style=\"width:100%; font-size:12px\" border=\"1\">\n")
        for file in sorted(os.listdir(statsDir), reverse=True):
            currentFile = os.path.join(statsDir, file)
            currentFileDate = file[:-4]
            finalData[currentFileDate] = []
            # checking if it is a file
            if os.path.isfile(currentFile):
                with open(currentFile, 'r') as currentStats:
                    for line in currentStats:
                        finalData[currentFileDate].extend([line.strip()])
            else:
                sys.exit(1)

        # Display stats for the last 10 days only.
        top10 = 0
        for key, value in finalData.items():
            allValues = ""
            if top10 < 10:
                for values in value:
                    allValues = allValues + "<td>" + values + "</td>"

                stats.write("<tr><td><strong>{0}:</strong></td><td>{1}</td></tr>".format(key, allValues))
                #print(key + ": " + allValues)
                top10 += 1
        stats.write("</table></body></html>\n")

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
    
    # generate page with stats from yesterdays logs
    with open(STATS_LOG_LOCATION+str(dateStamp)+".htm", 'w') as stats:
        for country, qty in sorted(hitsPerCountry.items()):
            stats.write("{0},{1}\n".format(country, str(qty)))

    # generate page from previously parsed stats pages
    generateStats("./stats")