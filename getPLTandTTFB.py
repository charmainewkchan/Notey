# Creates 2 CSV files with page load times and time to first byte for websites
# from all servers except Beijing.
# Command: python getPLTandTTFB.py (name of .txt file with websites) (name of CSV file)

import webbrowser
import time
import sys
import urllib2
import json
import csv
import copy

serverIDs = {
    "test":0,
    "ohio":0,
    "cal":0,
    "oregon":0,
    "canada":0,
    "saopaulo":0,
    "frankfurt":0,
    "ireland":0,
    "london":0,
    "paris":0,
    "mumbai":0,
    "tokyo":0,
    "seoul":0,
    "singapore":0,
    "sydney":0,
}

csv_columns = ['url', 'test', 'ohio', 'cal', 'oregon', 'canada', 'saopaulo', 'frankfurt', 'ireland', 'london', 'paris', 'mumbai', 'tokyo', 'seoul', 'singapore', 'sydney']

# dictionary of URL:url and all server:ttfb
URLandTTFBDict = {}

# dictionary of URL:url and all server:PLT
URLandPLTDict = {}

# Updates Dictionary of ID's
def getIDs(url):
    print("Getting ID's")
    for server in serverIDs:
        # run1 1st website  .ultrasite.com/api2/web/performance/speedtest?url=http://www.google.com
        response = urllib2.urlopen('http://' + server + '.ultrasite.com/api2/web/performance/speedtest?isMobile=0&url=' + url)
        html = response.read()
        #print(server + " has ID " + html + "\n")
        serverIDs[server] = html

# Returns single ttfb of server and ID
def getSingleTTFB(server, ID):
    #print('Getting SingleTTFB of server = ' + server + ', ID = ' + ID)
    response = urllib2.urlopen('http://' + server + '.ultrasite.com/api2/web/performance/tasks/list?id=' + ID)
    data = json.load(response)
    while data["data"]["tasks"]["status"] == 0:
        print("Sleeping 5 sec")
        time.sleep(5)
        response = urllib2.urlopen('http://' + server + '.ultrasite.com/api2/web/performance/tasks/list?id=' + ID)
        data = json.load(response)

    if data["data"]["tasks"]["webperformanceResult"]["result"] == "":
        TTFBtime = "N/A"
        pageLoadTime = "N/A"
        return TTFBtime, pageLoadTime

    result = data["data"]["tasks"]["webperformanceResult"]["result"][0]
    if result["finishedTime"] == 0:
        TTFBtime = "N/A"
        pageLoadTime = "N/A"

    else:
        TTFBtime = (result["finishedTime"] - result["requestTime"]) * 1000 - result["receiveHeadersEnd"]
        pageLoadTime =  data["data"]["tasks"]["webperformanceResult"]["totalTime"] / 1000
    return TTFBtime, pageLoadTime


def getAllData():
    print("Getting All TTFB for website")
    server_and_TTFB_dict = {}
    server_and_PLT_dict = {}
    for server in serverIDs:
        TTFBtime, pageLoadTime = getSingleTTFB(server, serverIDs[server])
        print("Server TTFB = " + server + " : " + str(TTFBtime) + " Page Load Time = " + str(pageLoadTime))
        server_and_TTFB_dict[server] = TTFBtime
        server_and_PLT_dict[server] = pageLoadTime
    return server_and_TTFB_dict, server_and_PLT_dict

def main():

    csvfile = open(sys.argv[2] + "_TTFB.csv", 'w')
    writer = csv.DictWriter(csvfile,fieldnames=csv_columns)
    writer.writeheader()

    csvfile2 = open(sys.argv[2] + "_PLT.csv", 'w')
    writer2 = csv.DictWriter(csvfile2,fieldnames=csv_columns)
    writer2.writeheader()


    websites = open(sys.argv[1] + ".txt", "r")
    for line in websites:
        print("website = " + line)

        # Updates ID's
        getIDs(line)
        URLandTTFBDict['url'] = line
        URLandPLTDict['url'] = line
        TTFBData, PLTData = getAllData()

        # Fill URLadnTTFBDict with server data
        URLandTTFBDict.update(TTFBData)
        URLandPLTDict.update(PLTData)
        #URLandTTFBDict.update(getAllData())

        # Add row to CSV
        writer.writerow(copy.deepcopy(URLandTTFBDict))
        writer2.writerow(copy.deepcopy(URLandPLTDict))

    print("Done!")

main()
