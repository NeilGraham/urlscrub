import os
from os.path import normpath, dirname, abspath, join, isfile
import json
from urllib.parse import urlparse
import pickle

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from modules.selenium.amazon import amazon_login, amazon_parse_product
from modules.selenium.bestbuy import bestbuy_login, bestbuy_parse_product

dir_script:str = abspath(join(normpath(dirname(__file__)), '..'))
dir_cookies:str = join(dir_script,"cache","cookies","_.pkl")

domain_meta = {
    'www.amazon.com': {
        'login':        amazon_login,
        'scrape':       amazon_parse_product,
        'credentials':  join(dir_script,'credentials','amazon.json'),
    },
    'www.bestbuy.com': {
        'login':        bestbuy_login,
        'scrape':       bestbuy_parse_product,
        'credentials':  join(dir_script,'credentials','bestbuy.json'),
    }
}


def scrape_urls(args, driver = None):
    res = []
    
    driver = webdriver.Firefox()
    
    # Set of domain names already logged into
    domains_logged_into = set()

    # Read cookies from file at location 'dir_cookies'
    cookies:list = pickle.load(open(dir_cookies, "rb")) if isfile(dir_cookies) else []

    # Iterate over each url specified
    for url in args.url:
        domain = urlparse(url).netloc
        
        # Throw error if domain is not in dict 'domain_meta'
        if domain not in domain_meta:
            raise ValueError("Unable to scrape domain: %s" % domain)
        
        login = domain_meta[domain].get('login')
        scrape = domain_meta[domain].get('scrape')
        
        # Log into domain if conditions are met
        if not (login == None or domain in domains_logged_into or args.skip_login):
            credentials = parse_domain_credentials(domain_meta[domain].get('credentials'))
            login(driver, credentials, cookies=cookies)
            domains_logged_into.add(domain)
        
        scrape_res = scrape(driver, url)
        res.append(scrape_res)
        
    # Save cookies to location 'dir_cookies'
    pickle.dump( driver.get_cookies() , open(dir_cookies,"wb"))

    driver.quit()
    
    return res

def parse_domain_credentials(path:str) -> dict[str]:
    with open(path, 'r') as f: data = json.load(f)
    return data