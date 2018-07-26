# Creates 2 CSV files with page load times and time to first byte for websites
# from Beijing server.
# Command: python3 getPLTandTTFB_Beijing.py (name of .txt file with websites) (name of CSV file)

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

# dictionary of URL:url and all server:ttfb
URLandTTFBDict = {}
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
def getTTFB(ID):
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
        TTFBTime = "N/A"
        pageLoadTime = "N/A"
    else:
        TTFBTime = (result["finishedTime"] - result["requestTime"]) * 1000 - result["receiveHeadersEnd"]
        pageLoadTime =  data["data"]["tasks"]["webperformanceResult"]["totalTime"] / 1000
    print("TTFB = " + str(TTFBTime))
    return TTFBTime, pageLoadTime

def main():
    websites = open(sys.argv[1] + ".txt", "r")
    csvfile = open(sys.argv[2] + "_Beijing_TTFB.csv", 'w')
    writer = csv.DictWriter(csvfile,fieldnames=csv_columns)
    writer.writeheader()

    csvfile2 = open(sys.argv[2] + "_Beijing_PLT.csv", 'w')
    writer2 = csv.DictWriter(csvfile2,fieldnames=csv_columns)
    writer2.writeheader()


    for line in websites:
        print("website = " + line)

        # Updates ID's
        getIDs(line)
        URLandTTFBDict['url'] = line
        URLandPLTDict['url'] = line

        # Fill URLadnTTFBDict with server data
        TTFBtime, pageLoadTime = getTTFB(serverIDs["beijing"])
        URLandTTFBDict["beijing"] = TTFBtime
        URLandPLTDict["beijing"] = pageLoadTime

        writer.writerow(copy.deepcopy(URLandTTFBDict))
        writer2.writerow(copy.deepcopy(URLandPLTDict))

    print("done!")

main()
