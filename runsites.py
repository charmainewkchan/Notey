# Opens Ultrasite speed test on browser for a list of websites (60s per test)

import webbrowser
import time
import sys

def run_sites(url):
    webbrowser.open("https://ultrasite.com/global_speed_audit.html?query=" + url)
    time.sleep(60)

def main():
    for i in range (0,1) :
        websites = open(sys.argv[1] + ".txt", "r")
        for line in websites:
            run_sites(line)
            print(line)
        print("test " + str(i) + " done!\n\n")
        websites.close()

main()
