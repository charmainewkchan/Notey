# Creates 1 CSV file with page load times for websites from Beijing server.
# Command: python3 getPLT_Beijing.py (name of .txt file with websites) (name of CSV file)

import webbrowser
import time
import sys
from urllib.request import urlopen
import json
import csv
import copy
import requests

serverIDs = {
    "beijing" : 0
}

csv_columns = ['url', 'beijing']

# list of URLandTTFBDict's
csv_data = []

# dictionary of URL:url and all server:plt
URLandPLTDict = {}


# Updates Dictionary of ID's
def getIDs(url):
    print("Getting ID")
    s = requests.Session()
    request = requests.Request('GET', 'https://www.ultrasite.com/api2/web/performance/speedtest/china?url=' + url + "&isMobile=0")
    prepared_request = s.prepare_request(request)
    settings = s.merge_environment_settings(prepared_request.url, None, None, None, None)
    response = s.send(prepared_request, **settings)

    html = str(response.text)
    html = html[1:-1]
    if html == "":
        serverIDs["beijing"] = "ERROR"
        print("ERROR")
        return
    print("ID = " + str(html))
    serverIDs["beijing"] = int(html)

# Returns single ttfb of server and ID
def getPLT(ID):
    print("Getting TTFB for website")
    if (ID == "ERROR"):
        return("ERROR")

    print("Requesting: https://www.ultrasite.com/api2/web/performance/tasks/list/china?id=" + str(ID))
    s = requests.Session()
    request = requests.Request('GET','https://www.ultrasite.com/api2/web/performance/tasks/list/china?id=' + str(ID))
    prepared_request = s.prepare_request(request)
    settings = s.merge_environment_settings(prepared_request.url, None, None, None, None)
    response = s.send(prepared_request, **settings)

    data = response.json()
    print(data)
    while data["data"]["tasks"]["status"] == 0:
        print("Sleeping 5 sec")
        time.sleep(5)
        request = requests.Request('GET', 'https://www.ultrasite.com/api2/web/performance/tasks/list/china?id=' + str(ID))
        prepared_request = s.prepare_request(request)
        response = s.send(prepared_request, **settings)
        data = response.json()

    result = data["data"]["tasks"]["webperformanceResult"]["result"][0]

    if result["finishedTime"] == 0:
        pageLoadTime = "N/A"
    else:
        pageLoadTime =  data["data"]["tasks"]["webperformanceResult"]["totalTime"] / 1000
    print("PLT = " + str(pageLoadTime))
    return pageLoadTime

def main():
    websites = open(sys.argv[1] + ".txt", "r")

    csvfile2 = open(sys.argv[2] + "_Beijing_PLTOnly.csv", 'w')
    writer2 = csv.DictWriter(csvfile2,fieldnames=csv_columns)
    writer2.writeheader()


    for line in websites:
        print("website = " + line)

        # Updates ID's
        getIDs(line)
        URLandPLTDict['url'] = line

        # Fill URLanePLTDict with server data
        pageLoadTime = getPLT(serverIDs["beijing"])
        URLandPLTDict["beijing"] = pageLoadTime

        writer2.writerow(copy.deepcopy(URLandPLTDict))

    print("done!")

main()
