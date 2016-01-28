'''
Run this file as `python main.py domain [--protocol https]` 
Example: python main.py jana.com
Example 2: python main.py jana.com --protocol https
'''

import sys
import argparse
from find_all_emails import GetEmails


def main(args):
    '''
    Runs the email finder and creates the arguments to parse through.
    '''
    email_scraper = GetEmails(args.domain, args.protocol)
    if not email_scraper.is_valid_domain(args.domain):
        print "Not a valid domain name."
        sys.exit(1)
    email_scraper.find_emails_in_site()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('domain', help='The domain name to get emails from')
    parser.add_argument('--protocol', default='http', help='Is the site http or https')
    args = parser.parse_args()
    if args.domain:
        main(args)
