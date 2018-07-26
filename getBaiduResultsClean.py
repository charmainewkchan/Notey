# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import csv
import re

USER_AGENT = {'User-Agent':'Chrome/61.0.3163.100'}
csv_columns = ['keyword', 1 , 2 , 3, 4 , 5 ,6 ,7 ,8 ,9 ,10 , 11, 12, 13, 14 , 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

csv_columns_set = ['link']
linkSet = {0,0}

prefix = re.compile('^(.)*//(www.)*')

postfix = re.compile('.com(.*)$')

def fetch_results(search_term, number_results):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')
    print ("search term = " + search_term)
    baidu_url = 'http://www.baidu.com/s?wd={}&pn={}'.format(escaped_search_term, number_results)
    response = requests.get(baidu_url, headers=USER_AGENT)
    response.raise_for_status()
    return search_term, response

def resolve_urls(url):
    try:
        final_url = requests.get(url, headers=USER_AGENT).url
    except requests.RequestException:
        return url
    else:
        return final_url


def parse_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')

    found_results = []
    rank = 1
    result_block = soup.find_all('div', attrs={'class': 'c-container'})
    for result in result_block:

        link = result.find('a', href=True)
        title = result.find('h3', attrs={'class': 't'})
        if link and title:

            link = link['href']
            link = resolve_urls(link)
            title = title.get_text()

            if link != '#':
                linkSet.add(link)
                found_results.append({'link': str(link), 'rank': rank})
                rank += 1
    return found_results


def scrape_baidu(search_term, number_results):
    try:
        keyword, html = fetch_results(search_term, number_results)
        results = parse_results(html.text, keyword)
        return results
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by baidu")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")


if __name__ == '__main__':
    csvfile = open("Baidu_CityAndHotel(Chinese)_ByRankURLS-2.csv", 'w')
    csvfile2 = open("Baidu_CityAndHotel(Chinese)_URLSUniqueSet-2.csv", 'w')

    writer = csv.DictWriter(csvfile,fieldnames=csv_columns)
    writer2 = csv.DictWriter(csvfile2,fieldnames=csv_columns_set)

    writer.writeheader()
    writer2.writeheader()


    keywords = open("CitiesChinese.txt").readlines()
    data = []
    dictOfOneQuery = {}


    for keyword in keywords:

        try:
            query = keyword[:-1] + "酒店"

            results = scrape_baidu(query, 5)
            dictOfOneQuery['keyword'] = query

            for result in results:
                print("keyword = " + dictOfOneQuery['keyword'] + " result['link'] = " + result['link'] + " result['rank'] = " + str(result['rank']))
                dictOfOneQuery[result['rank']] = result['link']

            writer.writerow(dictOfOneQuery)

        except Exception as e:
            print(e)
        finally:
            time.sleep(10)

    for url in linkSet:
        tempDict = {"link": url}
        writer2.writerow(tempDict)
