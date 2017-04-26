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

def is_not_image(self, link):
    '''
    Determines whether a given href is not an image
    '''
    image_tags = [".png", ".jpeg", ".jpg", ".gif"]
    return all([tag not in link for tag in image_tags])


def main(args):

    linkDictionary = {}
    phoneDictionary = {}
    deliveryDictionary = {}

    url = "https://www.allbud.com/dispensaries/massachusetts?results=80"
    text = urllib2.urlopen(url).read()
    soup = BeautifulSoup(text, "lxml")

    data = soup.findAll('div', attrs={'class':'title location truncate'})
    for div in data:
        links = div.findAll('a')
        for a in links:
            linkDictionary[a.contents[0]] = a['href']

    linkDictionary = collections.OrderedDict(sorted(linkDictionary.items()))

    for key, value in linkDictionary.iteritems():
        key.rstrip()
        url = "https://www.allbud.com" + value
        text = urllib2.urlopen(url).read()
        soup = BeautifulSoup(text, "lxml")

        #phone numbers
        data = soup.find('span', attrs={'itemprop':'telephone'})
        if data:
            phoneDictionary[key] = data.contents[0]
        else:
            phoneDictionary[key] = "None Found"

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

        print str(key) \
                + "\nPhone Number: " + str(phoneDictionary[key]) \
                + "\nDelivery Zones: " + str(deliveryDictionary[key]) + "\n"





    '''
    Runs the email finder and creates the arguments to parse through.
    '''
    # email_scraper = GetEmails(args.domain, args.protocol)
    # if not email_scraper.is_valid_domain(args.domain):
    #     print "Not a valid domain name."
    #     sys.exit(1)
    # email_scraper.find_emails_in_site()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('domain', help='The domain name to get emails from')
    parser.add_argument('--protocol', default='http', help='Is the site http or https')
    args = parser.parse_args()
    main(args)
