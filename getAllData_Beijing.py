# Creates 2 CSV files with page size, number of resources, and page load times/ time
# to first byte for websites from Beijing server.
# Command: python3 getAllData_Beijing.py (name of .txt file with websites) (name of CSV file)

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

csv_columns = ['url', 'PageSize', 'ResultLength', 'beijing']

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
def getAllData(ID):
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
        PageSize = "N/A"
        ResultLength = "N/A"
        TTFBTime = "N/A"
        pageLoadTime = "N/A"
    else:
        TTFBTime = (result["finishedTime"] - result["requestTime"]) * 1000 - result["receiveHeadersEnd"]
        pageLoadTime =  data["data"]["tasks"]["webperformanceResult"]["totalTime"] / 1000
    print("TTFB = " + str(TTFBTime))

    ResultLength = len(data["data"]["tasks"]["webperformanceResult"]["result"])
    if ResultLength == 0:
        PageSize = "N/A"
    else:
        PageSize =  data["data"]["tasks"]["webperformanceResult"]["totalByteSize"]/1000

    return PageSize, ResultLength, TTFBTime, pageLoadTime

def main():
    websites = open(sys.argv[1] + ".txt", "r")
    csvfile = open(sys.argv[2] + "_AllData_Beijing_TTFB.csv", 'w')
    writer = csv.DictWriter(csvfile,fieldnames=csv_columns)
    writer.writeheader()

    csvfile2 = open(sys.argv[2] + "_AllData_Beijing_PLT.csv", 'w')
    writer2 = csv.DictWriter(csvfile2,fieldnames=csv_columns)
    writer2.writeheader()


    for line in websites:
        print("website = " + line)

        # Updates ID's
        getIDs(line)
        URLandTTFBDict['url'] = line
        URLandPLTDict['url'] = line

        # Fill URLadnTTFBDict with server data
        PageSize, ResultLength, TTFBtime, pageLoadTime = getAllData(serverIDs["beijing"])
        URLandTTFBDict["beijing"] = TTFBtime
        URLandTTFBDict["PageSize"] = PageSize
        URLandTTFBDict["ResultLength"] = ResultLength

        URLandPLTDict["beijing"] = pageLoadTime
        URLandPLTDict["PageSize"] = PageSize
        URLandPLTDict["ResultLength"] = ResultLength

        writer.writerow(copy.deepcopy(URLandTTFBDict))
        writer2.writerow(copy.deepcopy(URLandPLTDict))

    print("done!")

main()
