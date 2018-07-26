import webbrowser
import time
import sys
import urllib2
import json
import csv
import copy
import re

csv_columns = ['keyword']

replacement_dict = {}

rewritten_line = {};

def main():

    csvfile = open("GoogleTTFBReplacements.csv", 'w')
    writer = csv.DictWriter(csvfile,fieldnames=csv_columns)
    writer.writeheader()

    for i in range(1,51):
        csv_columns.append(str(i))

    #print(csv_columns)

    replacements = csv.reader(open("GoogleTTFBKey.csv", 'rb'))
    lines_of_replacements = list(replacements)
    #print (lines_of_replacements)

    for line in lines_of_replacements:
        replacement_dict[line[0]] = line[1]

    data_sheet = csv.reader(open("GoogleTTFBPreReplace.csv", 'rb'))
    lines_of_data_sheet = list(data_sheet)

    for line in lines_of_data_sheet:
        rewritten_line['keyword'] = line[0]

        for i in range(1,51):

            for replacement_line in lines_of_replacements:
                if re.search(replacement_line[0], line[i]) != None:
                    #print(replacement_line[0] + " matches " + line[i])

                    rewritten_line[str(i)] = replacement_line[1]
                    break
                else:
                    rewritten_line[str(i)] = line[i]

        print("Writing line for " + rewritten_line['keyword'])
        #print(rewritten_line)

        writer.writerow(rewritten_line)

main()
