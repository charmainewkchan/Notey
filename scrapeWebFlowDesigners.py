# -*- coding: utf-8 -*-


import urllib2
#from bs4 import BeautifulSoup
import csv
import sys
import time
from datetime import datetime
import json
import random



url = "https://webflow.com/api/designers/popular?limit=12&offset="

csv_columns = ['First Name', 'Last Name', 'Username', 'About', 'Level', 'Hirable', 'Website', 'Country', 'City', 'Number of Webflow Sites' ]
info = {}

csvfile = open("Designers.csv", 'a')
writer = csv.DictWriter(csvfile,fieldnames=csv_columns)
#writer.writeheader()

for i in range(901,1001):
    print ("Page Number = " + str(i))

    page = urllib2.urlopen(url+str(i*12))
    time.sleep(random.randint(7,20))

    designers = json.load(page)

    for designer in designers:
        if ('firstName' in designer.keys()):
            info['First Name'] = designer["firstName"].encode('utf-8')
            #print(info['First Name'])
        else:
            info['First Name'] = ""

        if ('lastName' in designer.keys()):
            info['Last Name'] = designer["lastName"].encode('utf-8')
        else:
            info['Last Name'] = ""

        if ('username' in designer.keys()):
            info['Username'] = designer["username"].encode('utf-8')
        else:
            info['Username'] = "Unknown"

        if('about' in designer.keys()):
            info['About'] = designer["about"].encode('utf-8')
        else:
            info['About'] = ""

        if ('lvl' in designer.keys()):
            info['Level'] = designer["lvl"]
        else:
            info['Level'] = "Unknown"

        if ('hirable' in designer.keys()):
            info['Hirable'] = designer["hirable"]
        else:
            info['Hirable'] = "Unknown"

        if('website' in designer.keys()):
            info['Website'] = designer["website"].encode('utf-8')
        else:
            info['Website'] = ""
        #print(info['Website'])
        if('location' in designer.keys()):
            if('geoIpCountry' in designer["location"].keys()):
                info['Country'] = designer["location"]["geoIpCountry"].encode('utf-8')
            else:
                info['Country'] = "Unknown"

            if('geoIpCity' in designer["location"].keys()):
                info['City'] = designer["location"]["geoIpCity"].encode('utf-8')
            else:
                info['City'] = "Unknown"

        else:
            info['Country'] = ""
            info['City'] = ""

        #print(info['Country'])
        if ('pubSites' in designer.keys()):
            info['Number of Webflow Sites'] = len(designer["pubSites"])
        else:
            info['Number of Webflow Sites'] = 0

        #print(designer["firstName"])
        writer.writerow(info)
        #time.sleep(random.randint(1,2))
