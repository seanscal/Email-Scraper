'''
Run this file as `python main.py domain [--protocol https]` 
Example: python main.py jana.com
Example 2: python main.py jana.com --protocol https
'''

import sys
import argparse
from find_all_emails import GetEmails

from bs4 import BeautifulSoup
import urllib2
import lxml.html
import collections
import json
import os

def get_links(soup):

    linkDictionary = {}
    
    data = soup.findAll('div', attrs={'class':'title location truncate'})
    for div in data:
        links = div.findAll('a')
        for a in links:
            linkDictionary[a.contents[0]] = a['href']

    linkDictionary = collections.OrderedDict(sorted(linkDictionary.items()))

    return linkDictionary

def get_phone_numbers(key, soup):
    phoneDictionary = {}

    #phone numbers
    data = soup.find('span', attrs={'itemprop':'telephone'})
    if data:
        phoneDictionary[key] = data.contents[0]
    else:
        phoneDictionary[key] = "None Found"
    return phoneDictionary

def get_delivery_zones(key, soup):
    deliveryDictionary = {}

    #delivery zones
    data = soup.find('div', attrs={'id':'delivery-modal'})
    if data:
        body = data.find('div', attrs={'class':'modal-body'})
        contents = []
        
        if body.contents:
            for content in body.contents:
                stringToAdd = str(content).lstrip().split(" - ")[0]
                if "<br/>" not in stringToAdd and stringToAdd not in contents:
                    contents.append(stringToAdd)
                contents.sort()
            deliveryDictionary[key] = contents
        else:
            deliveryDictionary[key] = ["shouldnt be here"]
    else: 
        deliveryDictionary[key] = []

    return deliveryDictionary

def get_hours(key, soup):

    dayDict = {}
    hoursDict = {}
    dayArr = []
    hoursArr = []

    days = soup.findAll('span', attrs={'class':'dayname hidden-md'})
    for day in days:
        if day.contents:
            dayArr.append(day.contents[0])

    hours = soup.findAll('div', attrs={'class':'col-xs-5 col-sm-3 col-md-6 col-lg-5 hours'})
    for hour in hours:
        if hour.contents:
            hoursArr.append(hour.contents[0].lstrip().rstrip())
    # print hoursArr[0]

    for index in range(len(dayArr)):
        dayDict[dayArr[index]] = hoursArr[index]

    hoursDict[key] = dayDict
    return hoursDict


def main(args):
    
    url = "https://www.allbud.com/dispensaries/massachusetts?results=80"
    text = urllib2.urlopen(url).read()
    soup = BeautifulSoup(text, "lxml")

    linkDictionary = get_links(soup)

    jsonArray = []

    for key, value in linkDictionary.iteritems():
        key.rstrip()
        url = "https://www.allbud.com" + value
        text = urllib2.urlopen(url).read()
        soup = BeautifulSoup(text, "lxml")

        phoneDictionary = get_phone_numbers(key, soup)
        deliveryDictionary = get_delivery_zones(key, soup)
        hoursDict = get_hours(key, soup)

        data = {"name": key, 
                "phone": phoneDictionary[key], 
                "delivery_zones": deliveryDictionary[key],
                "hours": hoursDict[key]}
        jsonArray.append(data)

    os.remove("ChangedFile.csv")
    write_json(jsonArray)


def write_json(jsonArray):
    data = {}
    data['caretakers'] = jsonArray

    with open('caretakers.json', 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('domain', help='The domain name to get emails from')
    parser.add_argument('--protocol', default='http', help='Is the site http or https')
    args = parser.parse_args()
    main(args)
