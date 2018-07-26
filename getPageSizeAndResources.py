# Creates 1 CSV files with page size and number of resources.
# Command: python getPageSizeAndResources.py (name of .txt file with websites) (name of CSV file)

import webbrowser
import time
import sys
import urllib2
import json
import csv
import copy

serverIDs = {
    "test":0,
}

csv_columns = ['url', 'pageSize', "numOfResources"]

# dictionary of URL:url and all server:PLT
URLandPSDict = {}

# Updates Dictionary of ID's
def getIDs(url):
    print("Getting ID's")
    # run1 1st website  .ultrasite.com/api2/web/performance/speedtest?url=http://www.google.com
    response = urllib2.urlopen('http://test.ultrasite.com/api2/web/performance/speedtest?isMobile=0&url=' + url)
    html = response.read()
    #print(server + " has ID " + html + "\n")
    serverIDs["test"] = html

# Returns single ttfb of server and ID
def getSinglePS(ID):
    #print('Getting SingleTTFB of server = ' + server + ', ID = ' + ID)
    response = urllib2.urlopen('http://test.ultrasite.com/api2/web/performance/tasks/list?id=' + ID)
    data = json.load(response)
    while data["data"]["tasks"]["status"] == 0:
        print("Sleeping 5 sec")
        time.sleep(5)
        response = urllib2.urlopen('http://test.ultrasite.com/api2/web/performance/tasks/list?id=' + ID)
        data = json.load(response)

    if data["data"]["tasks"]["webperformanceResult"]["result"] == "":
        pageSize = "N/A"
        numOfResources = "N/A"
        return pageSize, numOfResources

    resultLength = len(data["data"]["tasks"]["webperformanceResult"]["result"])

    if resultLength == 0:
        pageSize = "N/A"
    else:
        pageSize =  data["data"]["tasks"]["webperformanceResult"]["totalByteSize"]/1000

    return pageSize, resultLength


def getAllData():
    print("Getting All PLT for website")
    PS_and_NOR_dict = {}

    pageSize, numOfResources = getSinglePS(serverIDs["test"])
    print("pageSize = " + str(pageSize) + ", numOfResources = " + str(numOfResources))
    PS_and_NOR_dict["pageSize"] = pageSize
    PS_and_NOR_dict["numOfResources"] = numOfResources

    return PS_and_NOR_dict


def main():
    csvfile2 = open(sys.argv[2] + "_PSandRLonly.csv", 'w')
    writer2 = csv.DictWriter(csvfile2,fieldnames=csv_columns)
    writer2.writeheader()

    websites = open(sys.argv[1] + ".txt", "r")
    for line in websites:
        print("website = " + line)

        # Updates ID's
        getIDs(line)
        URLandPSDict['url'] = line
        PLTData = getAllData()

        # Fill URLadnTTFBDict with server data
        URLandPSDict.update(PLTData)

        # Add row to CSV
        writer2.writerow(copy.deepcopy(URLandPSDict))

    print("done!")

main()
