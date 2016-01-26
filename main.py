import sys
import argparse
from find_all_emails import GetEmails


def main(args):
    email_scraper = GetEmails(args.domain)
    if not email_scraper.is_valid_domain(args.domain):
        print "Not a valid domain name."
        sys.exit(1)
    email_scraper.find_emails_in_site()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('domain')
    args = parser.parse_args()
    if args.domain:
        main(args)
    else:
    	"Please provide a domain argument"