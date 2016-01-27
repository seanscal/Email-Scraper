# Email-Scraper
Scrapes all emails from any given domain


#Installation Instructions

To use this app you should run

`python main.py domain`

in the command line


To install packages, the easiest way is to have homebrew (mac) and pip installed.

_Homebrew_ - `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"` in the command line

_pip_ - `sudo easy_install pip`

#Necessary Packages
_BeautifulSoup_ - `pip install beautifulsoup4` - for scraping webpages for data

_Selenium_ - `pip install selenium` - Allow javascript on pages to load

_PhantomJS_ - Mac: `brew install phantomjs`, Windows: http://phantomjs.org/download.html - Allows for headless testing of webpages.  

