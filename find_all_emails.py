import re
import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver


class GetEmails():
    '''
    Gets all the emails contained in a domain and prints them out.
    '''
    def __init__(self, domain, protocol):
        self.domain = domain
        self.links_visited = []
        self.emails = []
        self.protocol = protocol + "://"
        self.url = self.complete_domain_name(self.protocol)
        self.site_map = [self.url]
    def is_valid_domain(self, domain):
        '''
        Check if the domain entered is a valid domain.
        '''
        domain_regex = r'^[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*$'
        match = re.match(domain_regex, domain)
        if match:
            return True
        return False

    def complete_domain_name(self, protocol):
        '''
        Get the entire domain name, adding a '/' if one was not given
        '''
        complete_name = self.domain
        if not self.protocol in self.domain:
            complete_name = self.protocol + complete_name
        if complete_name[-1] != '/':
            complete_name = complete_name + '/'
        return complete_name


    def get_links_from_site(self, url, text):
        '''
        Get the links from each page using Beautiful Soup html parser.
        If the link does not contain the complete original domain or is invalid, it is not added.
        Also sped up a tiny bit by checking if the link is an image.
        '''
        soup = BeautifulSoup(text, 'html.parser')
        for link in soup.findAll('a', href=True):
            link = urlparse.urljoin(url, link.get('href'))
            if self.is_not_image(link) and self.should_explore(link):
                self.site_map.append(link)

    def is_not_image(self, link):
        '''
        Determines whether a given href is not an image
        '''
        image_tags = [".png", ".jpeg", ".jpg", ".gif"]
        return all([tag not in link for tag in image_tags])

    def should_explore(self, link):
        '''
        Decides whether to explore a given link
        '''
        if link in self.links_visited:
            return False
        if self.complete_domain_name(self.protocol) not in link:
            return False
        if link in self.site_map:
            return False

        return True

    def find_emails_in_site(self):
        '''
        Finds all of the emails in a single page, and then checks if there are any links
        which have not been added to the site map yet.  Does this until the site map is empty.
        PhantomJS is needed to allow the javascript on a page to populate the page before
        searching for links. This slows down the process but allows for a more complete search.
        '''
        email_regex = r'([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})'
        while self.site_map:
            url = self.site_map.pop()
            self.links_visited.append(url)

            driver = webdriver.PhantomJS()
            driver.get(url)
            text = driver.page_source

            emails = re.findall(email_regex, text, re.IGNORECASE | re.MULTILINE)
            for email in emails:
                if email not in self.emails:
                    self.emails.append(email)
            self.get_links_from_site(url, text)
        self.print_emails()

    def print_emails(self):
        '''
        Print results
        '''
        if self.emails:
            print 'Found these email addresses: '
            for email in self.emails:
                print email
        else:
            print 'No email addresses were found on this domain.'
