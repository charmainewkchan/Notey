import requests
from bs4 import BeautifulSoup
import time
import csv
import re

USER_AGENT = {'User-Agent':'Chrome/61.0.3163.100'}
csv_columns = ['rank', 'link', 'keyword']
csv_columns_set = ['link']
linkSet = {0,0}

prefix = re.compile('^(.)*//(www.)*')
postfix = re.compile('.com(.*)$')

def fetch_results(search_term, number_results, language_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')
    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return search_term, response.text


def parse_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')
    found_results = []
    rank = 1
    result_block = soup.find_all('div', attrs={'class': 'g'})

    for result in result_block:
        link = result.find('a', href=True)
        title = result.find('h3', attrs={'class': 'r'})
        description = result.find('span', attrs={'class': 'st'})
        if link and title:

            link = link['href']
            link = re.sub(postfix, ".com", link)
            link = re.sub(prefix, "", link)
            title = title.get_text()
            if description:
                description = description.get_text()
            if link != '#':
                linkSet.add(link)
                found_results.append({'keyword': str(keyword),'link': str(link), 'rank': rank})
                rank += 1
    return found_results


def scrape_google(search_term, number_results, language_code):
    try:
        keyword, html = fetch_results(search_term, number_results, language_code)
        results = parse_results(html, keyword)
        return results
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")


if __name__ == '__main__':
    csvfile = open("SwireResourcesURLS.csv", 'w')
    csvfile2 = open("SwireResourcesURLSGeneralset.csv", 'w')

    writer = csv.DictWriter(csvfile,fieldnames=csv_columns)
    writer2 = csv.DictWriter(csvfile2,fieldnames=csv_columns_set)

    writer.writeheader()
    writer2.writeheader()


    keywords = ['site:swire-resources.com', 'site:spcschina.com' ]
    data = []

    for keyword in keywords:
        try:
            sleep(2)
            results = scrape_google(keyword, 2, "en")
            for result in results:
                print("Single result: ")
                print(result)
                writer.writerow(result)
                data.append(result)

        except Exception as e:
            print(e)
        finally:
            time.sleep(10)

    for url in linkSet:
        tempDict = {"link": url}
        writer2.writerow(tempDict)
